import requests
import json
import os
from urllib.request import urlretrieve
from .models import Genre, Platform, Game
from django.core.files import File


def get_platforms():
    url = 'https://api.rawg.io/api/platforms?key=648630fcff3e4ba29e9cedfc5b4da76c'
    r = requests.get(url)
    for result in r.json()['results']:
        rawg_id = result['id']
        name = result['name']
        slug = result['slug']
        Platform.objects.create(name=name, slug=slug, rawg_id=rawg_id)


def get_genres():
    url = 'https://api.rawg.io/api/genres?key=648630fcff3e4ba29e9cedfc5b4da76c'
    r = requests.get(url)
    for result in r.json()['results']:
        rawg_id = result['id']
        name = result['name']
        slug = result['slug']
        Genre.objects.create(name=name, slug=slug, rawg_id=rawg_id)


def get_games(platform: str):
    url = (
        'https://api.rawg.io/api/games?key=648630fcff3e4ba29e9cedfc5b4da76c&platforms=' + platform
    )
    currnet_platform = Platform.objects.get(rawg_id=int(platform))
    while url is not None:
        responce = requests.get(url)
        for result in responce.json()['results']:
            name = result['name']
            image_name = result['slug'] + '.jpg'
            urlretrieve(result['background_image'], image_name)
            game = Game(name=name, platform=currnet_platform)
            game.image.save(image_name, File(open(image_name, 'rb')))
            game.save()
            if os.path.exists(image_name):
                os.remove(image_name)
            for genre in result['genres']:
                genre = Genre.objects.get(rawg_id=genre['id'])
                game.genre.add(genre)
            game.save()
        url = responce.json()['next']
