import configparser
import requests
import json
import os

def set_last_round(config, year, month, day, round):
    config['meta']['LastRound'] = f"{year}/{month:02}/{day:02}/{round}"
    if os.path.exists('config.ini'):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        with open('/opt/KeepWatcher/config.ini', 'w') as configfile:
            config.write(configfile)

def check_if_round_ended(config, round_path):
    gamelog = f"{config['meta']['LogPath']}/{round_path}/game.log"
    with open(gamelog) as f:
        lines = f.read().splitlines()
        if "GAME: The round has ended." in lines:
            return True

def send_webhook(webhook, username=None, avatar_url=None, content=None, file=None, embeds=None):
    data = {}
    if username:
        data["username"] = username
    if content:
        data["content"] = content
    if avatar_url:
        data["avatar_url"] = avatar_url
    if embeds:
        if not isinstance(embeds, list):
            embeds = [embeds]
        data["embeds"] = embeds

    headers = {'Content-Type': 'application/json'}

    if file:
        files = {'file': (file, open(file, 'rb'))}
        r = requests.post(webhook, files=files, data={'payload_json': json.dumps(data)})
    else:
        r = requests.post(webhook, json=data, headers=headers)

    return r
