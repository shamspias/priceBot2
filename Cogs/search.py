import asyncio
from itertools import *
from collections import Counter

import discord
from variables import *
from checks import *
from discord.ext import commands
from discord.ext.commands import command
from phonetics import metaphone
from pymongo.collation import Collation, CollationStrength
db = cluster["Main"]
collection = db["Items"]

class search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @command(pass_context=True, aliases=['p'])
    async def price(self, ctx, *, arg=None):
        arg1 = arg.split()
        try:
            args = arg1[1]
        except:
            args = None
        try:
            types = arg1[2]
        except:
            types = None

        if arg == None:

            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Price Help')
            embed.set_thumbnail(url=Coin)

            embed.add_field(name=f'{ctx.prefix}price (name of item)', value='Search an Item.', inline=False)
            #embed.add_field(name=f'{ctx.prefix}price changes', value='Check for item price changes for today', inline=False)

            await ctx.send(embed=embed)


        elif arg == 'changes':
            None # TODO Add features


        elif arg1[0].upper() == 'DYE':
            dye = db["Dye"]
            count = dye.count_documents({"name": args})
            typo = ["staff", "knuckles", "OHS", "THS", "halberd", "MD", "katana", "bow", "bowgun", "armour",
                    "additional"]
            if args == None:
                info = []
                look = dye.find()
                for x in look:
                    info.append(f"\n•**Dye {x['name']}**")
                s1 = ''
                info.sort()
                embed = discord.Embed(
                    description=s1.join(info),
                    title='',
                    colour=0xfb607f
                )
                embed.set_author(name='Dye List')
                embed.set_thumbnail(url=Monocle)

                await ctx.send(embed=embed)

            elif types == None or types not in typo:
                info = []
                for x in typo:
                    info.append(f"\n•**{x}**")
                s1 = ''
                info.sort()
                embed = discord.Embed(
                    description=s1.join(info),
                    title=f'{ctx.prefix}price dye {args} (dye item type)',
                    colour=0xfb607f
                )
                embed.set_author(name='Dye Item Types')
                embed.set_thumbnail(url=Monocle)

                await ctx.send(embed=embed)

            elif count == 1:
                embed = discord.Embed(
                    description='',
                    title='',
                    colour=0xfb607f
                )
                embed.set_author(name=f"Dye {args}")
                i = dye.find_one({"name": args})
                try:
                    embed.set_thumbnail(url=i["color"])
                except:
                    None
                try:
                    embed.add_field(name=f"{types}:",
                                    value=(
                                    f"Part A: **{i[types]['part A']}**\n"
                                    f"Part B: **{i[types]['part B']}**\n"
                                    f"Part C: **{i[types]['part C']}**"
                                    ),
                                    inline=False
                                    )
                except:
                    None
                try:
                    embed.set_footer(text=f"Edited on: {i['edited on']}")
                except:
                    None

                await ctx.send(embed=embed)

            else:
                await ctx.send("> Dye not Found")

        #
        else:

            #names = [name for name in arg.split()]
            index = [metaphone(l) for l in arg.split()]
            try:
                info1 = [x['name'] for x in collection.find({"name": arg}).collation(Collation(locale='en', strength=CollationStrength.SECONDARY))]
                print(info1)
            except:
                info1 = []
            try:
                test = [x for x in collection.find({"name": arg})]
                print(test)
            except:
                pass
            if len(info1) == 0:
                whole = [text['name'] for text in collection.find({"$text": {"$search": f"\"{arg}\""}})]
                print(f"Full: {whole}")
                info1 = whole
            if len(info1) == 0:
                meta = [text['name'] for text in collection.find({"search id": metaphone(arg)})]
                print(f"Full Metaphone: {meta}")
                info1 = meta
            if len(info1) == 0:
                split = [text['name'] for argument in arg.split() for text in collection.find({"$text": {"$search": argument}})]
                print(f"Individual Text: {split}")
                regex = [text['name'] for x in index for text in collection.find({"search id": {"$regex": f".*{x}.*", "$options": 'i'}})]
                print(f"Regex Search ID: {regex}")
                info1 = split + regex
            #print(info1)
            #if len(info1) == 0:
                print("reserve")
                start = 0
                end = 3
                while True:
                    start = start
                    end = end
                    text = arg[start:end]
                    for info in collection.find({"name": {"$regex": f".*{text}.*", "$options": 'i'}}):
                        info1.append(info['name'])
                    start += 1
                    end += 1
                    if end > len(arg):
                        break
            if len(info1) != 1:
                info1.sort()
                list1 = Counter(info1)
                res1 = list1.most_common()
                mix = [int(x) for l in res1 for x in str(l[1])]
                info = [arg[0] for arg in res1 if arg[1] == max(mix)]
                info = list(dict.fromkeys(info))
            else:
                info = list(dict.fromkeys(info1))

            # If not more than one
            if len(info) == 0 or len(info) == None:
                await ctx.send("> Item not Found/ Item not Added")


            elif len(info) == 1:
                name = info[0]
                look2 = collection.find_one({"name":name})

                embed = discord.Embed(
                    description='',
                    title='',
                    colour=0xfb607f
                )
                embed.set_author(name=f"{name}")
                try:
                    embed.set_thumbnail(url=look2["item type"])
                except:
                    pass

                embed.add_field(name="Price:", value=look2['price'], inline=False)

                try:
                    embed.add_field(name="NPC Price:", value=look2["npc"], inline=False)
                except:
                    pass

                try:
                    embed.add_field(name="•note", value=look2["note"], inline=False)
                except:
                    pass

                try:
                    if (is_moderator2(ctx) or is_editor2(ctx)) and ctx.guild.id == server:
                            edited_by = look2["edited by"]
                            edited_by = await self.bot.fetch_user(edited_by)
                            embed.add_field(name="Edited by:", value=f"{edited_by.name}#{edited_by.discriminator}", inline=False)

                    embed.set_footer(text=f"Edited on: {look2['edited on']}")

                except:
                    pass

                await ctx.send(embed=embed)



            else:
                s1 = "**\n•**"
                page = 1
                counter = 1
                pages = {}
                cur_page = 1
                for results in info:
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
                    description=f"\n•**{s1.join(menu_page)}**",
                    title='',
                    colour=0xfb607f
                )
                embed.set_author(name='Did you Mean?')
                embed.set_thumbnail(url=Monocle)
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
                                    description=f"\n•**{s1.join(menu_page)}**",
                                    title='',
                                    colour=0xfb607f
                                )
                                embed.set_author(name='Did you Mean?')
                                embed.set_thumbnail(url=Monocle)
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
                                    description=f"\n•**{s1.join(menu_page)}**",
                                    title='',
                                    colour=0xfb607f
                                )
                                embed.set_author(name='Did you Mean?')
                                embed.set_thumbnail(url=Monocle)
                                embed.set_footer(text=f"Page: {cur_page}")
                                await menu.edit(embed=embed)

                                await menu.remove_reaction(reaction, user)

                            else:
                                await menu.remove_reaction(reaction, user)
                        except asyncio.TimeoutError:
                            await menu.clear_reactions()
                            break





def setup(bot):
    bot.add_cog(search(bot))

