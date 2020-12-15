from scripts.util import discussions_query

import pydash
import requests

PROBLEMS_URL = 'https://leetcode.com/api/problems/all/'

class Problem(object):
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
  for p in sorted(problems, key=lambda p: p.question_id):
    print(f"Processing {p.question_id}")
    resp = discussions_query.execute(p.question_id)
    discussions_data = pydash.get(resp.json(), 'data.questionTopicsList.edges')
    p.set_discussion_titles([extract_title(json) for json in discussions_data])
    print(f"Done processing {p.question_id}!")
  # store in a postgres instance

if __name__ == '__main__':
  scrape()