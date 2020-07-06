from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.debug = True

client = Elasticsearch()




@app.route('/', methods=['GET'])
def index():
    return "Flask works!"

@app.route('/client/info', methods=['GET'])
def client_info():
    return {
        'content-type': 'application/json',
        'user_agent': str(request.user_agent)
    }

@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_id(movie_id):
    if request.method == 'GET':
        #https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
        body = {
                "_source": ["genre", "director", "description", "writers", "writers_names", "actors", "actors_names", "title", "imdb_rating"], "query": {
                    "match": {
                        "_id": movie_id
                        }
                    }
                }

        res = client.search(index="movies", doc_type="_doc", body=body)

        res = res['hits']['hits']
        id = res[0]['_id']
        source = res[0]['_source']

        genre = source['genre']
        director = source['director']
        title = source['title']
        description = source['description']
        imdb_rating = source['imdb_rating']

        writers = source['writers']
        writers_names = source['writers_names'].split(',')
        actors = source['actors']
        actors_names = source['actors_names'].split(',')

        for i in range(len(writers)):
            writers[i]['name'] = writers_names[i].strip()

        for i in range(len(actors)):
           actors[i]['name'] = actors_names[i].strip()

        result_dict = {'id': id, 'genre': [genre], 'director': [director], 'writers': writers, 'title': title, 'description': description, 'imdb_rating': imdb_rating, 'actors': actors}

        return jsonify(result_dict)



@app.route('/api/movies', methods=['GET'])
def api_movies():
    if request.method == 'GET':
        limit = request.args.get('limit', type = int)
        page = request.args.get('page', type = int)
        search = request.args.get('search', type = str).strip('/"')
        sort = request.args.get('sort', type = str).strip('/"')
        sort_order = request.args.get('sort_order', type = str).strip('/"')

        #https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-sort.html
        body = {
                "size": limit,
                "_source": ["title", "imdb_rating"],
                "sort": [{sort: sort_order}],
                "query": {
                    "match": {
                        "title": search
                        }
                    }
                }

        res = client.search(index="movies", doc_type="_doc", body=body)
        res = res['hits']['hits']

        movies_list = []
        for i in range(len(res)):
            movie = {"id": res[i]['_id'], "title": res[i]['_source']['title'], "imdb_rating": res[i]['_source']['imdb_rating'] }
            movies_list.append(movie)

        return jsonify(movies_list)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

#venv_praktikum
#python app/run.py