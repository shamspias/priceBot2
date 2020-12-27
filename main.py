import discord
from checks import *
from variables import *
from discord.ext import commands
import logging
import os
from pymongo import MongoClient
from pymongo.collation import Collation

db = cluster["Main"]
collection = db["main"]
Var = db["Var"]
items = db["Items"]

logging.basicConfig(level=logging.INFO)

def get_prefix(bot, message):
	results = collection.find({"_id":message.guild.id})
	for result in results:
		return str(result["prefix"])


bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'Toram | @me'))
    print("Bot is Ready")

@bot.event
async def on_member_join(member):
	embed = discord.Embed(
		description=f'**{member.name}** Has Joined the Server',
		title='**Welcome!**',
		colour=0xffdf00
	)
	embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
	embed.set_thumbnail(url=member.guild.icon_url)
	embed.set_footer(text=f'Members: {member.guild.member_count}')
	channel = bot.get_channel(740104361211854919)
	await channel.send(embed=embed)

@bot.event
async def on_guild_join(guild):
	collection.insert_one({"_id":guild.id, "prefix":"."})

@bot.event
async def on_guild_remove(guild):
	collection.delete_one({"_id":guild.id})

@bot.command()
@commands.is_owner()
async def register(ctx):
	collection.insert_one({"_id":ctx.guild.id, "prefix": "."})

@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def changeprefix(ctx, prefix):
	collection.update_one({"_id":ctx.guild.id}, {"$set": {"prefix":prefix}})
	await ctx.send(f"> Prefix changed to ``{prefix}``")

# Cog Commands
@bot.command()
async def load1(ctx, extension):
	bot.load_extension(f'Cogs.{extension}')

@bot.command()
async def unload1(ctx, extension):
	bot.unload_extension(f'Cogs.{extension}')

for filename in os.listdir('./Cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'Cogs.{filename[:-3]}')

@bot.command()
@commands.is_owner()
async def createinv(ctx):
	invite = await ctx.channel.create_invite()
	print(invite)
	await ctx.send(f"Here's your invite: {invite}")


@bot.command()
async def inv(ctx):
	
	embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
	)
	embed.set_author(name='Invites!')
	embed.set_thumbnail(url=Info)
	#embed.add_field(name="My Invite:", value="https://discord.com/api/oauth2/authorize?client_id=786125997271416833&permissions=116736&scope=bot",  inline=False)
	embed.add_field(name="Toram Price List Server:", value="Join and contribute to the prices!\nhttps://discord.gg/W4hxqPk6eH", inline=False)
	embed.add_field(name="Phantom Library Invite:", value="https://discord.gg/8xTgjqd ", inline=False)
	await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def var(ctx, var, *, link):
	Var.update_one({"_id":0}, {"$set": {var:link}})
	await ctx.send(f"> Added {var}:{link}")


@bot.command()
@commands.is_owner()
async def say1(ctx, channel, *, msg):
	channel = bot.get_channel(int(channel))
	await channel.send(msg)

@bot.command()
@commands.is_owner()
async def dyechange(ctx, dye1):
	try:
		dye = db["Dye"]
		dye.update({"name": dye1},
				   {"$set": 
						{
							"bow": {"part A": 1, "part B": 1, "part C": 1},
							"OHS": {"part A": 1, "part B": 1, "part C": 1},
							"THS": {"part A": 1, "part B": 1, "part C": 1},
							"staff": {"part A": 1, "part B": 1, "part C": 1},
							"katana": {"part A": 1, "part B": 1, "part C": 1},
							"bowgun": {"part A": 1, "part B": 1, "part C": 1},
							"halberd": {"part A": 1, "part B": 1, "part C": 1},
							"knuckles": {"part A": 1, "part B": 1, "part C": 1},
							"MD": {"part A": 1, "part B": 1, "part C": 1}
						}
					})
		await ctx.send(f"> Updated **{dye1}**")
	except:
		await ctx.send("> Failed")

@bot.command()
@commands.is_owner()
async def changevar(ctx, type, *, link):
	item = db["Items"]
	count = item.count_documents({"item type": type})
	if count == 1:
		search = item.find({"item type": type})
		for x in search:
			item.update_one({"_id":x["_id"]},
							{"$set":
								 {
									 "item type": link
								  }
							})
		await ctx.send("Updated")
	else:
		await ctx.send("> Could not find items")

@bot.command()
@commands.is_owner()
async def test5(ctx):
    await ctx.send("Got it")
    items.create_index('name', collation=Collation(locale='en', strength=2))
    await ctx.send("Done")
    

@bot.command()
@commands.is_owner()
async def color(ctx, var, *, link):
	try:
		dye = db["Dye"]
		dye.update_one({"name": var},
					   {"$set":
							{
								"color": link
							}
					   }
					   )
	except:
		await ctx.send("> Dye Number not Found")


try:
	token = os.environ['TOKEN']
except:
	pass


bot.run(token)
