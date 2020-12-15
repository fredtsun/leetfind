'''
yeah... this could be modeled better but meh..
its a small bulk of the entire thing that i dont anticipate changing,
probably the only place where graphql is going to be used in here anyways?
'''
import requests

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

def execute(question_id):
  return requests.post(ENDPOINT, json={
    'query': QUERY,
    'variables': VARIABLES % question_id,
    'operationName': OPNAME})

