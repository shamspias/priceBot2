import discord
from variables import *
from discord.ext import commands
from discord.ext.commands import command
from pymongo import MongoClient

db = cluster["Main"]
collection = db["Categories"]

class items(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
    async def item(self, ctx, *, arg=None):
        try:
            search = collection.find({"under":arg})
        except:
            await ctx.send("> Not Found")


        desc = []
        s1 = ''

        for look in search:
            if "name" in look.keys():
                print(look)
                print(look["name"])
                desc.append(f"\n**•{look['name']}**")

            embed = discord.Embed(
                description=f"\n{s1.join(desc)}",
                title='',
                colour=0xfb607f
            )
            embed.set_author(name=arg)
            embed.set_thumbnail(url=Scroll)

            await ctx.send(embed=embed)










def setup(bot):
    bot.add_cog(items(bot))