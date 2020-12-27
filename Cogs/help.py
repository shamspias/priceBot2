import asyncio

import discord
from variables import *
import checks
from checks import *
from discord.ext import commands
from discord.ext.commands import command
from pymongo import MongoClient

db = cluster["Main"]
collection = db["Categories"]
bot_id = "<@786125997271416833>"
bot_id2 = "<@!786125997271416833>"

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        message2 = message.content.split()
        try:
            if message2[0] == bot_id or message2[0] == bot_id2:
                prefix = await self.bot.get_prefix(message)
                embed = discord.Embed(
                    title=f'Hello {message.author.name}!',
                    description=f'My prefix is **{prefix}**\n**{prefix}help** for more info.'
                )
                await channel.send(embed=embed)
        except:
            None


    @command(pass_context=True)
    async def list(self, ctx, arg=None):
        if arg == None:

            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='List Help')
            embed.set_thumbnail(url=Info)

            embed.add_field(name=f'{ctx.prefix}list main', value='Main Categories.', inline=False)
            embed.add_field(name=f'{ctx.prefix}list (name of category)', value="Display the categories/items in the category", inline=False)


            await ctx.send(embed=embed)

        elif arg == "main":
            categories = collection.find({"type": "main"})

            desc = []
            s1 = ''

            for look in categories:
                name = look["name"]
                desc.append(f"\n**•{name}**\n")



            embed = discord.Embed(
                description=s1.join(desc),
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Main Categories')
            embed.set_thumbnail(url=Scroll)

            await ctx.send(embed=embed)

            #.list (name)
        else:

            arg = arg.lower()
            arg = arg.capitalize()
            count1 = collection.count_documents({"under": arg})
            count2 = collection.count_documents({"name": arg})
            search = collection.find({"under": arg})

            desc1 = [f"•{x['name']}" for x in collection.find({"under": arg, "type": "sub"})]
            desc2 = [f"-{x['name']}" for x in collection.find({"under": arg, "type": "item"})]
            desc3 = [f"-Dye {x['name']}" for x in collection.find({"under": arg, "type": "dye"})]
            desc = desc1 + desc2 + desc3
            search2 = collection.find({"link": arg})
            for look2 in search2:
                name2 = look2["name"]
                desc.append(f"-{name2}")

            if count1 != 0 and count2 != 0:
                s1 = "**\n**"
                desc.sort()
                desc.sort(key=arrange)
                page = 1
                counter = 1
                pages = {}
                cur_page = 1
                for results in desc:
                    if page in pages:
                        pages[page].append(results)
                    else:
                        pages[page] = [results]
                    counter += 1
                    if counter == 6:
                        page += 1
                        counter = 1
                page = len(pages.keys())
                menu_page = [values for values in pages[cur_page]]

                embed = discord.Embed(
                    description=f"\n**{s1.join(menu_page)}**",
                    title=check_type(arg),
                    colour=0xfb607f
                )
                embed.set_author(name=arg)
                embed.set_thumbnail(url=Scroll)
                embed.set_footer(text=f"Page: {cur_page}")

                if cur_page == page:
                    embed.set_footer(text="Last Page")
                    await ctx.send(embed=embed)
                else:
                    embed.set_footer(text=f"Page: {cur_page}")
                    menu = await ctx.send(embed=embed)
                    await menu.add_reaction(left)
                    await menu.add_reaction(right)
                    pending[ctx.author] = menu.id
                    while True:
                        if pending[ctx.author] != menu.id:
                            await menu.clear_reactions()
                            break
                        try:
                            reaction, user = await self.bot.wait_for(
                                'reaction_add',
                                timeout=30,
                                check=lambda reaction, user: user == ctx.author \
                                                             and str(reaction.emoji) in [left, right]
                            )
                            emote = str(reaction.emoji)
                            if emote == right and cur_page != page:
                                cur_page += 1

                                menu_page = [values for values in pages[cur_page]]
                                embed = discord.Embed(
                                    description=f"\n**{s1.join(menu_page)}**",
                                    title=check_type(arg),
                                    colour=0xfb607f
                                )
                                embed.set_author(name=arg)
                                embed.set_thumbnail(url=Scroll)

                                if cur_page == page:
                                    embed.set_footer(text="Last Page")
                                else:
                                    embed.set_footer(text=f"Page: {cur_page}")
                                await menu.edit(embed=embed)

                                await menu.remove_reaction(reaction, user)

                            elif emote == left and cur_page > 1:
                                cur_page -= 1

                                menu_page = [values for values in pages[cur_page]]
                                embed = discord.Embed(
                                    description=f"\n**{s1.join(menu_page)}**",
                                    title=check_type(arg),
                                    colour=0xfb607f
                                )
                                embed.set_author(name=arg)
                                embed.set_thumbnail(url=Scroll)

                                embed.set_footer(text=f"Page: {cur_page}")
                                await menu.edit(embed=embed)
                                await menu.remove_reaction(reaction, user)

                            else:
                                await menu.remove_reaction(reaction, user)


                        except asyncio.TimeoutError:
                            await menu.clear_reactions()
                            break


            elif count2 == 1 and count1 == 0:
                await ctx.send("> No Sub Categories / Items added yet")


            else:
                await ctx.send("> Category not Found")








    @command(pass_context=True)
    async def help(self, ctx, arg=None):
        if arg == None:
            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )

            embed.set_author(name='Help!')
            embed.set_thumbnail(url=Info)
            embed.add_field(name=f'{ctx.prefix}inv', value='My Invite!', inline=False)
            embed.add_field(name=f'{ctx.prefix}price (name)', value='Search the Price of an Item', inline=False)
            #embed.add_field(name=f'{ctx.prefix}price changes', value="Check for Today's Price Changes", inline=False)
            embed.add_field(name=f'{ctx.prefix}list', value='List for items.', inline=False)
            embed.add_field(name=f'{ctx.prefix}help mod', value='Commands for Moderators/Admins', inline=False)

            if is_in_server2(ctx) and is_editor2(ctx):
                embed.add_field(name='\u200b', value='\u200b', inline=False)
                embed.add_field(name=f'{ctx.prefix}help change', value='Commands for changing the price', inline=False)
                if is_moderator2(ctx):
                    embed.add_field(name=f'{ctx.prefix}help edit', value='Commands for editing the list', inline=False)
                    embed.add_field(name=f'{ctx.prefix}approve', value='Approval commands for prices', inline=False)

            embed.set_footer(text="Sponsor: Phantom Library")
            await ctx.send(embed=embed)

        elif arg == "mod" and commands.has_guild_permissions(manage_guild=True):

            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Mod Help')
            embed.set_thumbnail(url=Info)
            embed.add_field(name=f'{ctx.prefix}changeprefix  (prefix)', value='Change my prefix!', inline=False)
            embed.set_footer(text="Sponsor: Phantom Library")
            await ctx.send(embed=embed)

        elif arg == 'edit' and is_in_server2(ctx) and is_moderator2(ctx):

            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Editing Help')
            embed.set_thumbnail(url=Info)
            embed.add_field(name=f'{ctx.prefix}edit main add (name)', value='Add a Main category', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit main delete (name)', value='Delete a main category', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit sub add (name)', value='Add a Sub category', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit sub delete (name)', value='Delete a Sub category', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit item add (Category/Subcategory) (item type) (item name)', value='Add an Item', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit item delete (name)', value='Delete an Item', inline=False)
            embed.add_field(name=f'{ctx.prefix}edit rename (category/item name)', value='Rename a category/item', inline=False)

            await ctx.send(embed=embed)

        elif arg == 'change' and is_in_server2(ctx)and is_editor2(ctx):
            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Price Change Help')
            embed.set_thumbnail(url=Info)

            embed.add_field(name=f'\n\n{ctx.prefix}changeprice', value='Commands for changing the item price', inline=False)
            if is_moderator2(ctx):
                embed.add_field(name=f'\n\n{ctx.prefix}changenpcprice', value='Commands for setting item NPC prices', inline=False)
                embed.add_field(name=f'\n\n{ctx.prefix}changeitemnote', value='Commands for setting item note', inline=False)
                embed.add_field(name=f'\n\n{ctx.prefix}changedyeprice', value='Commands for setting dye prices', inline=False)

            await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(help(bot))
