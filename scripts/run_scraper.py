import pydash
import requests

PROBLEMS_URL = 'https://leetcode.com/api/problems/all/'


class Problem(object):
    BASE_URL = 'https://leetcode.com/problems/{slug}'

    def __init__(self, json):
        stats = json['stat']
        self.question_id = stats['question_id']
        self.question_id_display = stats['frontend_question_id']
        self.title = stats['question__title']
        self.slug = stats['question__title_slug']
        self.frequency = json['frequency']
        self.paid_only = json['paid_only']
        self.discussion_titles = []

    def set_discussion_titles(self, discussion_titles):
        self.discussion_titles = discussion_titles

    @property
    def url(self):
        return self.BASE_URL.format(slug=self.slug)

    def __str__(self):
        join_token = '🔥🥳'
        fields = [
            self.title,
            self.question_id_display,
            self.url,
            ' '.join(self.discussion_titles)
        ]
        return join_token.join([str(f) for f in fields])


class DiscussionQuery(object):
    '''yeah... this could be modeled better but meh..
    its a small bulk of the entire thing that i dont anticipate changing,
    probably the only place where graphql is going to be used in here anyways?
    '''
    ENDPOINT = 'https://leetcode.com/graphql'

    QUERY = """query questionTopicsList(
      $questionId: String!
      $orderBy: TopicSortingOption
      $skip: Int
      $query: String
      $first: Int!
      $tags: [String!]
    ) {
      questionTopicsList(
        questionId: $questionId
        orderBy: $orderBy
        skip: $skip
        query: $query
        first: $first
        tags: $tags
      ) {
        ...TopicsList
        __typename
      }
    }
    fragment TopicsList on TopicConnection {
      totalNum
      edges {
        node {
          id
          title
          commentCount
          viewCount
          pinned
          tags {
            name
            slug
            __typename
          }
          post {
            id
            voteCount
            creationDate
            isHidden
            status
            __typename
          }
          lastComment {
            id
            post {
              id
              author {
                isActive
                username
                profile {
                  userSlug
                  __typename
                }
                __typename
              }
              peek
              creationDate
              __typename
            }
            __typename
          }
          __typename
        }
        cursor
        __typename
      }
      __typename
    }"""

    VARIABLES = """{
      "orderBy": "most_votes",
      "query":"",
      "skip": 0,
      "first":25,
      "tags":[],
      "questionId":%s
    }"""

    OPNAME = "questionTopicsList"

    @classmethod
    def execute(cls, question_id):
        return requests.post(cls.ENDPOINT, json={
            'query': cls.QUERY,
            'variables': cls.VARIABLES % question_id,
            'operationName': cls.OPNAME})


def get_problems():
    resp = requests.get(PROBLEMS_URL)
    assert 200 <= resp.status_code < 300, "Error on request for LeetCode problems"
    json_resp = resp.json()
    assert 'stat_status_pairs' in json_resp, "Missing `stat_status_pairs` key in response"
    return [Problem(json) for json in json_resp['stat_status_pairs']]


def extract_title(json):
    return pydash.get(json, 'node.title') or ''


def scrape():
    problems = get_problems()
    with open("leetfind.txt", "w+") as f:
        for p in sorted(problems, key=lambda p: p.question_id):
            print(f"Processing {p.question_id}")
            resp = DiscussionQuery.execute(p.question_id)
            discussions_data = pydash.get(
                resp.json(), 'data.questionTopicsList.edges')
            p.set_discussion_titles([extract_title(json)
                                     for json in discussions_data])
            f.write(str(p) + '\n')
            print(f"Done processing {p.question_id}!")


if __name__ == '__main__':
    scrape()
