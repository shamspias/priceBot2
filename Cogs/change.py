import asyncio

import discord
from variables import *
from checks import *
from typing import Optional
from discord.ext import commands
from discord.ext.commands import command
from phonetics import metaphone
import datetime

db = cluster["Main"]
collection = db["Items"]
collection2 = db["Approve"]



class change(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
    @is_editor()
    @is_in_server()
    async def changeprice(self, ctx, price=None, *, args=None):

        if price == None or args == None :
            await ctx.send(f"> {ctx.prefix}changeprice (price) (item name)")

        elif is_moderator2(ctx):
            count = collection.count_documents({"name": args})
            if count != 1:
                await ctx.send("> Could not find the exact item")

            else:
                try:
                    price = price.split('|')
                    price = '\n'.join(price)
                except:
                    pass
                collection.update_one({"name": args},
                                      {"$set":
                                           {"price": price,
                                            "edited on": now,
                                            "edited by": ctx.author.id
                                           }
                                      })
                await ctx.send(f"> Edited price of **{args}** to:\n**{price}**")

        else:
            search = collection.find({"name":args})
            count = collection.count_documents({"name":args})
            if count != 1:
                await ctx.send("> Could not find the exact item")

            else:
                for x in search:
                    count = collection2.count_documents({"name": args})
                    print(count)
                    if count != 0:
                        delete = collection2.find_one({"name": args})
                        collection2.delete_one(delete)
                    
                    try:
                        price = price.split('|')
                        price = '\n'.join(price)
                    except:
                        pass
                    collection2.insert_one({"name": args, "edited by": ctx.author.id, "edited on": now, "price": price})

                    embed = discord.Embed(
                        description=f"Changing price to:\n**{price}**",
                        title=args,
                        colour=0xfb607f
                    )
                    embed.set_author(name='Change Price')
                    embed.set_thumbnail(url=x["item type"])
                    embed.set_footer(text='To Be Approved by Moderators')

                    await ctx.send(embed=embed)

    @command(pass_context=True)
    @is_moderator()
    @is_in_server()
    async def changenpcprice(self, ctx, price=None, *, args=None):

        if price == None or args == None:
            await ctx.send(f"> {ctx.prefix}changenpcprice (price/remove) (item name)")

        elif price == "remove":
            search = collection.find_one({"name": args})
            count = collection.count_documents({"name": args})
            if count != 1:
                await ctx.send("> Could not find the exact item")
            else:
                collection.update_one({"_id": search["_id"]},
                                      {"$unset":
                                           {"npc": ""}
                                       }
                                      )
                await ctx.send(f"> Removed NPC price of **{args}**")

        else:
            search = collection.find_one({"name":args})
            count = collection.count_documents({"name":args})
            if count != 1:
                await ctx.send("> Could not find the exact item")

            else:
                collection.update_one({"_id":search["_id"]},
                                      {"$set":
                                           {"npc":price}
                                       }
                                      )
                await ctx.send(f"> Updated NPC price of **{args}** to **{price}**")


    @command(pass_context=True)
    @is_moderator()
    @is_in_server()
    async def changeitemnote(self, ctx, *, args=None):
        count = collection.count_documents({"name": args})
        art = args.split()
        print(art[0])
        if args == None:
            await ctx.send(f"> {ctx.prefix}changeitemnote (item name/reset)")

        elif art[0] == "reset":
            arg = art[1:]
            name = ' '.join(arg)
            count = collection.count_documents({"name": name})
            if len(arg) == 0:
                await ctx.send(f"> {ctx.prefix}changeitemnote reset (name)")
            else:
                if count != 1:
                    await ctx.send("> Could not find item")

                else:
                    collection.update_one({"name": name},
                                          {"$unset":
                                               {"note": ""}
                                           }
                                          )
                    await ctx.send(f"> Removed **{name}**'s description")



        elif count != 1:
            await ctx.send("> Could not find item")

        else:
            send = await ctx.send("> Please input note...")
            try:
                msg = await self.bot.wait_for(
                    "message",
                    timeout=60,
                    check=lambda message: message.author == ctx.author \
                                          and message.channel == ctx.channel
                )
                if msg:
                    await send.delete()
                    await msg.delete()
                    collection.update_one({"name": args},
                                          {"$set":
                                               {"note": msg.content}
                                           }
                                          )

                    await ctx.send(f"**{args}** description set to:\n**{msg.content}**")

            except asyncio.TimeoutError:
                await send.delete()
                await ctx.send("> Cancelling...", delete_after=10)

    @command(pass_context=True)
    @is_editor()
    @is_moderator()
    @is_in_server()
    async def changedyeprice(self, ctx, dye_num=None, dye_type=None,part1=None, part2=None, part3=None):
        def part(part):
            try:
                return int(part)
            except:
                if part == "keep":
                    return "keep"
                else:
                    raise commands.BadArgument

        typo = ["staff", "knuckles", "OHS", "THS", "halberd", "MD", "katana", "bow", "bowgun", "armour",
                    "additional"]
        if dye_num == None or dye_type == None:
            await ctx.send(f"> {ctx.prefix}changedyeprice (dye number) (dye item type) (part A) (part B) (part C)")
        elif dye_type not in typo:
            info = []
            for x in typo:
                info.append(f"\n•**{x}**")
            s1 = ''
            info.sort()
            embed = discord.Embed(
                description=s1.join(info),
                title='Error',
                colour=0xfb607f
            )
            embed.set_author(name='Dye item types')
            embed.set_thumbnail(url=Monocle)

            await ctx.send(embed=embed)
        elif part1 == None or part2 == None or part3 == None:
            await ctx.send(f"> Missing Prices\n> If you want to keep the previous prices type in `keep`\n> **Example:**\n> {ctx.prefix}changeprice 05 weapon 1000000 keep 1000000")
        else:
            part1 = part(part1)
            print(part1)
            part2 = part(part2)
            print(part2)
            part3 = part(part3)
            dye = db["Dye"]
            count = dye.count_documents({"name": dye_num})
            if count != 1:
                s1 = ''
                lists = []
                loop = dye.find()
                for x in loop:
                    lists.append(f"\n•**Dye {x['name']}**")
                embed = discord.Embed(
                    description=s1.join(lists),
                    title='Dye Numbers',
                    colour=0xfb607f
                )
                embed.set_author(name="Error")
                embed.set_thumbnail(url=Info)

                await ctx.send(embed=embed)

            else:
                if part1 == 'keep':
                    l = dye.find_one({"name": dye_num})
                    part1 = l[dye_type]['part A']

                if part2 == 'keep':
                    l = dye.find_one({"name": dye_num})
                    part2 = l[dye_type]['part B']

                if part3 == 'keep':
                    l = dye.find_one({"name": dye_num})
                    part3 = l[dye_type]['part C']

                dye.update({"name": dye_num}, {"$set":
                                                   {
                                                       dye_type: {"part A": part1, "part B": part2, "part C": part3},
                                                       "edited on": now
                                                   }
                                               })

                await ctx.send(f"Set Dye **{dye_num}** price of **{dye_type}** to:\n"
                               f"•Part A: **{part1}**\n"
                               f"•Part B: **{part2}**\n"
                               f"•Part C: **{part3}**"
                               )




    @command(pass_context=True)
    @is_moderator()
    @is_in_server()
    async def approve(self, ctx, *, arg=None):

        if arg == None:
            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Approval Commands')
            embed.set_thumbnail(url=Info)

            embed.add_field(name=f'{ctx.prefix}approve list', value='List of items to approve', inline=False)
            embed.add_field(name=f'{ctx.prefix}approve all', value='Approve all item prices', inline=False)
            embed.add_field(name=f'{ctx.prefix}approve (item name)', value="Approve an item price change", inline=False)
            embed.add_field(name=f'{ctx.prefix}disapprove (item name)', value="Disapprove an item price change", inline=False)

            await ctx.send(embed=embed)

        elif arg == "all":

            all = collection2.find()

            for x in all:
                print(x)
                find = collection.find_one({"name":x["name"]})
                print(find)
                collection.update_one({"_id": find["_id"]}, {"$set": {"price": x["price"]}})
                collection.update_one({"_id": find["_id"]}, {"$set": {"edited by": x["edited by"]}})
                collection.update_one({"_id": find["_id"]}, {"$set": {"edited on": x["edited on"]}})

                collection2.delete_one(x)

            await ctx.send("> Approved **all**")

        elif arg == "list":

            look = collection2.find()

            embed = discord.Embed(
                description='',
                title='',
                colour=0xfb607f
            )
            embed.set_author(name='Approval List')
            embed.set_thumbnail(url=Info)

            for x in look:
                print(x)
                name = x["name"]
                old = collection.find_one({"name": name})
                print(old)
                old = old["price"]
                new = x["price"]
                edited_on = x["edited on"]
                edited_by = x["edited by"]
                edited_by = await self.bot.fetch_user(edited_by)

                embed.add_field(name=f'-{name}', value=f'**{old}** >> **{new}**\nEdited: **{edited_by.name}#{edited_by.discriminator}**\n{edited_on}', inline=False)

            await ctx.send(embed=embed)


        else:
            print("YES")
            count2 = collection2.count_documents({"name":arg})
            if count2 == 1:
                find = collection.find_one({"name":arg})
                x = collection2.find_one({"name":arg})
                collection.update_one({"_id":find["_id"]}, {"$set": {"price": x["price"]}})
                collection.update_one({"_id":find["_id"]}, {"$set": {"edited by": x["edited by"]}})
                collection.update_one({"_id":find["_id"]}, {"$set": {"edited on": x["edited on"]}})

                collection2.delete_one(x)

                await ctx.send(f"> Successfully approved **{arg}**")

            else:
                await ctx.send(f"> Could not Find {arg}")

    @command(pass_context=True)
    @is_moderator()
    @is_in_server()
    async def disapprove(self, ctx, *, arg=None):

        if arg == None:
            await ctx.send(f"> {ctx.prefix}disapprove (item name)")

        else:
            count2 = collection2.count_documents({"name": arg})
            if count2 == 1:
                x = collection2.find_one({"name": arg})
                collection2.delete_one(x)

                await ctx.send(f"> Successfully disapproved **{arg}**")

            else:
                await ctx.send(f"> Could not Find {arg}")




def setup(bot):
    bot.add_cog(change(bot))
