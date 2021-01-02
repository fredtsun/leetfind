from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

import os
import subprocess

app = Flask(__name__, static_folder='client/build', static_url_path='/')
api = Api(app)
cors = CORS(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


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
    port = 80 if os.getenv('ENV').lower() == 'prod' else 3000
    app.run(port=port)
