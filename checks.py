import discord
from variables import *
from discord.ext import commands
from discord.ext.commands import command

db = cluster["Main"]
collection = db["Categories"]


async def owner(ctx):
    if await ctx.bot.is_owner(ctx.author):
        return True
    else:
        return False



def is_in_server():
    async def predicate(ctx):
        return ctx.guild.id == server

    return commands.check(predicate)

def is_in_server2(ctx):
    if ctx.guild.id == server:
        return True

def is_moderator():
    async def predicate(ctx):
        return commands.has_role(moderator)

    return commands.check(predicate)

def is_moderator2(ctx):
    roles = [role.id for role in ctx.author.roles]
    if moderator in roles:
        return True
    else:
        return False

def is_editor():
    async def predicate(ctx):
        return commands.has_role(editor)

    return commands.check(predicate)

def is_editor2(ctx):
    roles = [role.id for role in ctx.author.roles]
    if editor in roles:
        return True
    else:
        return False

def is_item(name):
    try:
        search = collection.find_one({"name":name})
        if "item" in search["type"]:
            return True
    except:
        None


def is_dye(name):
    try:
        search = collection.find_one({"name":name})
        if "dye" in search["type"]:
            return True
    except:
        None


def is_subcat(name):
    try:
        search = collection.find_one({"name":name})
        if "sub" in search["type"]:
            return True
    except:
        None


def is_maincat(name):
    try:
        search = collection.find_one({"name": name})
        if "main" in search["type"]:
            return True
    except:
        None

def no_duplicate(arg):
    count = collection.count_documents({"name":arg})
    if count == 0:
        return True

def check_id(name):
    look = collection.find_one({"name":name})
    print(type(look["_id"]))
    return str(look["_id"])

def delete_item(name):
    collection2 = db["Items"]
    delete = collection2.find_one({"name":name})
    collection2.delete_one(delete)

def delete_dye(name):
    collection = db["Dye"]
    delete = collection.find_one({"name":name})
    collection.delete_one(delete)

def check_type(name):
    look = collection.find_one({"name":name})
    try:
        if look["type"] == "sub":
            return "Sub Category"

        elif look["type"] == "item":
            return "Item"

        else:
            return "Main Category"
    except:
        None

def to_int(arg):
    try:
        return int(arg)
    except:
        return None

def arrange(arg):
    if '•' in arg:
        return 0
    elif '-' in arg:
        return 1


















