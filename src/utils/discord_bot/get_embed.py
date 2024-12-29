import discord
from discord.ext import commands

kind2title = {
    "i" : "Issue",
    "pr" : "Pull Request",
    "r" : "Release",
    "c" : "Commit"
}

def get_embed(kind, obj):
    embed = discord.Embed(
        title = get_title(kind, obj),
        # url=obj['html_url'],
        description=f"New {kind2title[kind]} Updated\n\n{obj['html_url']}",
        color=discord.Color.blue()
    )

    name, avatar_url = get_author(kind, obj)
    embed.set_author(name=name, icon_url=avatar_url)

    return embed


def get_title(kind, obj):
    title = ""
    if kind == "i" or kind == "pr":
        title = f"[{kind2title[kind]}] " + ("Update: " if obj['flag_updated'] else "") + obj['title']
    elif kind == "r":
        title = f"[Release] {obj['name']}"
    elif kind == "c":
        title = f"[Commit] {obj['commit']['message']}"

    return title

def get_author(kind, obj):
    name = ""
    avatar_url = ""

    if kind == "i" or kind == "pr":
        name = obj['user']['login']
        avatar_url = obj['user']['avatar_url']
    elif kind == "r" or kind =="c":
        name = obj['author']['login']
        avatar_url = obj['author']['avatar_url']
    
    return name, avatar_url
        