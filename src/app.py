import os
import json
import time
import discord
import asyncio
import threading
from datetime import datetime, timezone, timedelta

from utils.github_api import *
from utils.discord_bot import *

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")

def check_and_send(repo, last_check_time):
    if repo["release"]:
        r_update = github_check_release(last_check_time, GITHUB_API_TOKEN, repo)
        if r_update.get("update", False):
            for d in r_update['data']:
                notify_to_channel("r", repo['repository'], d)

    if repo["issue"]["check"]:
        i_update = github_check_issue(last_check_time, GITHUB_API_TOKEN, repo)
        if i_update.get("update", False):
            for d in i_update['data']:
                notify_to_channel("i", repo['repository'], d)

    if repo["pull_request"]["check"]:
        pr_update = github_check_pull_request(last_check_time, GITHUB_API_TOKEN, repo)
        if pr_update.get("update", False):
            for d in pr_update['data']:
                notify_to_channel("pr", repo['repository'], d)

    if repo["commit"]["check"]:
        c_update = github_check_commit(last_check_time, GITHUB_API_TOKEN, repo)
        if c_update.get("update", False):
            for d in c_update['data']:
                notify_to_channel("c", repo['repository'], d)

def notify_to_channel(kind, channel, obj):
    intents = discord.Intents.default()
    bot = DiscordBot(intents=intents, guild_id=DISCORD_GUILD_ID)
    
    embed = get_embed(kind=kind, obj=obj)
    bot.set_channel(channel=channel)
    bot.set_message(embed=embed)

    bot.run(token=DISCORD_BOT_TOKEN)
        

def main():
    last_check_time = str((datetime.now(timezone.utc) - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"))

    while True:
        with open("repo.json", "r") as file:
            repositories = json.load(file)

        threads = []
        for repo in repositories:
            th = threading.Thread(target=check_and_send, args=(repo, last_check_time))
            threads.append(th)
            th.start()
        
        last_check_time = str(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

        for th in threads:
            th.join()

        time.sleep(600)


if __name__ == "__main__":
    main()