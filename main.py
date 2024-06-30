import configparser
import requests
import logging
import json
import os
import sys
import helpers

config = configparser.ConfigParser()
config.read('config.ini')

if config['meta']['DebugLoggingPath'] != "":
    logging.basicConfig(filename=config['meta']['DebugLoggingPath'], level=logging.INFO)
    logging.info(f"Logging started, saving to {config['meta']['DebugLoggingPath']}")
else:
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging started")

if config['meta']['GetMostRecentLogs']:
    logging.info("Getting most recent logs")
    year = max(map(int, os.listdir(config['meta']['LogPath'])))
    month = max(map(int, os.listdir(f"{config['meta']['LogPath']}/{year}")))
    day = max(map(int, os.listdir(f"{config['meta']['LogPath']}/{year}/{month:02}")))
    round = sorted(os.listdir(f"{config['meta']['LogPath']}/{year}/{month:02}/{day:02}"))[-1]
    round_path = f"{year}/{month:02}/{day:02}/{round}"
    logging.info(f"Using most recent logs at {round_path}")
else:
    # TODO
    raise NotImplementedError("Getting log manually is not implemented yet")

if config['meta']['SkipProcessedRounds'] == "yes" and config['meta']['LastRound'] == round_path:
    logging.info("Round already processed, skipping and exiting")
    sys.exit(0)

if config['features']['Manifest'] == "yes":
    logging.info("Starting manifest processing")
    with open(f"{config['meta']['LogPath']}/{round_path}/manifest.log") as f:
        manifest = f.read().splitlines()[2:]
    manifest = list(map(lambda x: x.split(" \\ "), manifest))
    formatted_manifest = "\n".join([f"**{x[1]}** the **{x[2]}** was played by **{x[0]}**" for x in manifest])
    formatted_manifest = "\n".join(sorted(formatted_manifest.split("\n"), key=lambda x: x.split(" ")[1]))
    logging.info(f"Manifest processed, sending webhook")
    embed = {
        "title": f"Weekly Census",
        "description": formatted_manifest,
        "footer": {
            "text": f"{round_path}"
        }
    }
    r = helpers.send_webhook(config['features.manifest']['WebhookAddress'], embeds=[embed])
    logging.info("Webhook sent")
    logging.info(f"Response: {r.text}")

helpers.set_last_round(config, year, month, day, round)
logging.info("Last round updated")