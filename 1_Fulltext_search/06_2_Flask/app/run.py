from flask import Flask, request
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.debug = True




@app.route('/', methods=['GET'])
def index():
    return "Flask works!"


@app.route('/client/info', methods=['GET'])
def client_info():
    return {
        'content-type': 'application/json',
        'user_agent': str(request.user_agent)
    }

@app.route('/api/v1/movies/{MOVIE_ID}', methods=['GET'])
def movie_id():
    if request.method == 'GET':
         data = request.args

    return str(data)

@app.route('/api/movies', methods=['GET'])
def api_movies():

    if request.method == 'GET':
        data = request.args
        # dataDict = json.loads(data)

        #?limit=1&page=1&sort=id&sort_order=asc&search=

        # args = request.args
        # args1 = request.args.get('limit')
        # args2 = request.args.get('sort')
        # args3 = request.args.get('sort_order')
        # args4 = request.args.get('search')

    return str(data)
    # return {
    #     'content-type': 'application/json',
    #     'user_agent': str(data)
    # }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

#venv_praktikum
#python app/run.py