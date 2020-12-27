import discord
from variables import *
from checks import *
from discord.ext import commands
from pymongo import MongoClient

@is_in_server()
async def item_type(ctx):
    desc = []
    s1 = ''

    for keys in item_types:
        desc.append(f"\n**•{keys}**")

    embed = discord.Embed(
        description=f"\n{s1.join(desc)}",
        title='Item Types',
        colour=0xfb607f
    )
    embed.set_author(name='Error')
    embed.set_thumbnail(url=Info)

    await ctx.send(embed=embed)

