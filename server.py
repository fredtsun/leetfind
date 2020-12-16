from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

import subprocess

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

class Search(Resource):
    def get(self, search_term):
        res = subprocess.run(
            ['rg', '-i', '-N',  search_term, 'leetfind.txt'], capture_output=True, text=True)
        lines = res.stdout.split('\n')
        resp = []
        for l in lines:
            if not l:
                continue
            title, q_id, url, _ = l.split('🔥🥳')
            resp.append({
                'title': title,
                'question_id': q_id,
                'url': url
            })
        return {'data': resp}

api.add_resource(Search, '/<search_term>')

if __name__ == '__main__':
    app.run()
