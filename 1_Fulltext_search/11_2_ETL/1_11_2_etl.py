from pathlib import Path
import json
import sqlite3

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk




def get_raw_movie_table(cursor):
    print('--> get_raw_movie_table')
    q = """SELECT id as _id, imdb_rating, genre, title, plot as description, director, writer, writers FROM movies"""
    res = cursor.execute(q)
    res = [dict(row) for row in res.fetchall()]

    for row in res:
        try:
            row['imdb_rating'] = float(row['imdb_rating'])
        except ValueError:
            del row['imdb_rating']
    return res


def add_writers_id_and_names(raw_movie_table, cursor):
    print('--> add_writers_id_and_names')
    movie_table = []

    for row in raw_movie_table:
        writers_in_row = []
        # приводим содержимое колонки writer к виду содержимого колонки writers
        if row['writer'] and not row['writers']:
            writers_in_row.append({'id': row['writer']})
            del row['writer']

        if row['writers'] and not row['writer']:
            writers_in_row.extend(json.loads(row['writers']))
            del row['writer']

        row['writers'] = writers_in_row

        # заполняем writers_names по ID из writers
        if writers_in_row:
            writers_names = []
            for id in writers_in_row:
                q = """SELECT name FROM writers WHERE id='{0}'""".format(id['id'])
                res = cursor.execute(q)
                writers_names.append(res.fetchone()[0])
            # перечисялем через запятую
            row['writers_names'] = ', '.join([i for i in writers_names])

        movie_table.append(row)
    return movie_table


def add_actors_id_and_names(transform_movie_table, cursor):
    print('--> add_actors_id_and_names')
    movie_table = []

    # достаём actor_id по movie_id
    for row in transform_movie_table:
        if row['_id']:
            movie_id = row['_id']
            q = """SELECT actor_id FROM movie_actors WHERE movie_id='{0}'""".format(movie_id)
            res = cursor.execute(q)
            res = [dict(act) for act in res.fetchall()] #{'actor_id': '1'}

        # заполянем actors диктами с ID актёров
        if res:
            actors_id = []
            for actor_id in res:
                actors_id.append({'id': actor_id['actor_id']}) #{'id': '1'}
            row['actors'] = actors_id

            # заполянем actors_names по ID
            if actors_id:
                actors_names = []
                for id in actors_id:
                    q = """SELECT name FROM actors WHERE id='{0}'""".format(id['id'])
                    res = cursor.execute(q)
                    actors_names.append(res.fetchone()[0])
                # перечисялем через запятую
                row['actors_names'] = ', '.join([i for i in actors_names])

        movie_table.append(row)
    return movie_table


def sqlite_connect(sqlite_dump_path):
    conn = sqlite3.connect(sqlite_dump_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_index(elastic_client, elastic_index_path, elastic_index_name):
    print('--> create_index')
    with open(elastic_index_path, 'r') as f:
        es_schema = f.read()
    elastic_client.indices.create(index=elastic_index_name, body=es_schema, ignore=400)



def run():
    current_dir = Path.cwd()
    sqlite_dump_path = str(current_dir / 'db.sqlite')
    elastic_index_path = str(current_dir / 'es_schema.txt')

    conn = sqlite_connect(sqlite_dump_path)
    cursor = conn.cursor()

    print('Start transforming table')
    raw_table = get_raw_movie_table(cursor)
    transform_table = add_writers_id_and_names(raw_table, cursor)
    transform_table = add_actors_id_and_names(transform_table, cursor)
    conn.close()

    print('Start loading to Elasticsearch')
    client = Elasticsearch()
    create_index(client, elastic_index_path, 'movies')
    result = bulk(client, index='movies', actions=transform_table)

    print('Loaded {0} rows, {1} errors'.format(result[0], len(result[1])))


"""     transform_table
   {
      "index": {
         "_index": "movies",
         "_type": "_doc",
         "_id": "tt0076759",
         "data": {
            "imdb_rating": "8.6",
            "genre": "Action, Adventure, Fantasy, Sci-Fi",
            "title": "Star Wars: Episode IV - A New Hope",
            "description": "The Imperial Forces, under orders from cruel Darth Vader",
            "director": "George Lucas",
            "writers": "[{'id': '0b60f2f38d7ef03db580c18d214a403eb0877b34'}, {'id': '0b60f2f35988f621775659dbb7ad784c3795d71b'}, {'id': '0b60f2f348adc2f668a9a090165e24f3d3a7cf5a'}]",
            "writers_names": "George Lucas",
            "actors": "[{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '5'}]",
            "actors_names": "Mark Hamill, Harrison Ford, Carrie Fisher, Peter Cushing"
         }
      }
   }
"""

if __name__ == "__main__":
    run()
