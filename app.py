from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('video_game', user='postgres', password='2345', host='localhost', port='5432')

class BaseModel(Model):
    class Meta:
        database = db

class VideoGame(BaseModel):
    title = CharField()
    genre = CharField()
    release_year = IntegerField()

db.connect()
db.drop_tables([VideoGame])
db.create_tables([VideoGame])

VideoGame(title='The Witcher 3: Wild Hunt', genre='Action RPG', release_year=2015).save()
VideoGame(title='Cyberpunk 2077', genre='Action RPG', release_year=2020).save()
VideoGame(title='Assassin\'s Creed Valhalla', genre='Action Adventure', release_year=2020).save()
VideoGame(title='Call of Duty: Warzone', genre='Battle Royale', release_year=2020).save()
VideoGame(title='Among Us', genre='Social Deduction', release_year=2018).save()

app = Flask(__name__)

@app.route('/video_game/', methods=['GET', 'POST'])
@app.route('/video_game/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(VideoGame.get(VideoGame.id == id)))
        else:
            game_list = []
            for game in VideoGame.select():
                game_list.append(model_to_dict(game))
            return jsonify(game_list)

    if request.method == 'PUT':
        body = request.get_json()
        VideoGame.update(body).where(VideoGame.id == id).execute()
        return "Video Game " + str(id) + " has been updated."

    if request.method == 'POST':
        new_game = dict_to_model(VideoGame, request.get_json())
        new_game.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        VideoGame.delete().where(VideoGame.id == id).execute()
        return "Video Game " + str(id) + " deleted"

app.run(debug=True, port=5000)
