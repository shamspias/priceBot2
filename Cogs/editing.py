import asyncio
from itertools import zip_longest as zips
import discord
from embeds import *
import variables
from checks import *
from discord.ext import commands
from discord.ext.commands import command
from pymongo import MongoClient
from phonetics import metaphone






db = cluster["Main"]
collection = db["Categories"]

class editing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #
    @command(pass_context=True)
    @is_in_server()
    @is_moderator()
    async def edit(self, ctx, arg1=None, arg2=None, arg3=None, arg4=None, *, arg5=None):



        if arg1 == "main":
            # .edit main add (name)
            if arg2 == "add" and arg4 == None:
                collection.insert_one({"type": "main", "name": arg3})
                await ctx.send(f"> Added **{arg3}**")


            # .edit main delete (name)
            elif arg2 == "delete" and await owner(ctx):
                if is_maincat(arg3) == True:

                    under2 = [arg3]
                    while len(under2) != 0:

                        var = under2.pop()
                        try:
                            under = collection.find({"under": var})
                            for x in under:
                                print(x)
                                try:
                                    search = collection.find({"under": x["name"]})
                                    for x2 in search:
                                        under2.append(x2["name"])
                                except:
                                    pass
                                if x["type"] == "item":
                                    delete_item(x["name"])
                                    collection.delete_one(x)

                                elif x["type"] == "dye":
                                    delete_dye(x["name"])
                                    collection.delete_one(x)

                                else:
                                    collection.delete_one(x)
                        except:
                            pass

                        delete = collection.find_one({"name":var})
                        if is_item(var) == True:
                                 print("Is Item")
                                 delete_item(delete["name"])
                                 collection.delete_one(delete)
                        else:
                            collection.delete_one(delete)

                    await ctx.send(f"> Deleted **{arg3}**")


                else:
                    await ctx.send("> Main Category does not exist")
            elif arg4 != None:
                await ctx.send("> Spaces are not Allowed")




        # Subcategories
        elif arg1 == "sub":
            # .edit sub add (main) (name)
            if arg2 == "add":
                count = no_duplicate(arg4)
                if arg4 != None and arg5 == None and count == True and (is_maincat(arg3) == True or is_subcat(arg3) == True): # TODO Item Check
                    collection.insert_one({"type":"sub", "under":arg3, "name":arg4})
                    await ctx.send(f"> Added subcatgory **{arg4}** in **{arg3}**")

                elif arg4 == None:
                    await ctx.send("> Missing Name")

                elif arg5 != None:
                    await ctx.send("> Spaces are not Allowed")

                elif count != True:
                    await ctx.send("> Duplicate Category Found")

                else:
                    await ctx.send("> Category not Found")



            # .edit sub delete (subcategory)
            elif arg2 == "delete" and await owner(ctx):
                try:
                    if is_subcat(arg3) == True:
                        under3 = [arg3]
                        # TODO Change name to ID
                        while len(under3) != 0:

                            under2 = under3.pop()
                            under = collection.find({"under":under2})
                            for x in under:
                                print(x)
                                try:
                                    search = collection.find({"under":x["name"]})
                                    for x2 in search:
                                        under3.append(x2["name"])
                                except:
                                    pass
                                	
                                if x["type"] == "item":
                                    delete_item(x["name"])
                                    collection.delete_one(x)

                                elif x["type"] == "dye":
                                    delete_dye(x["name"])
                                    collection.delete_one(x)
                                
                                else:
                                    collection.delete_one(x)

                            delete = collection.find_one({"name":under2})

                            if is_item(under2) == True:
                                delete_item(delete["name"])
                                collection.delete_one(delete)
                            else:
                                collection.delete_one(delete)



                        await ctx.send(f"> Deleted **{arg3}**")

                    else:
                        await ctx.send("> Sub Category not Found")
                except:
                    await ctx.send("> Could not delete the category")

            else:
                await ctx.send("> Command does not exist")


        # ==========================================================================================

        elif arg1 == "item":
            # .edit item add (Category/Subcategory) (item type) (item name)
            if arg2 == "add" and arg5 != None:
                count = no_duplicate(arg5)
                if arg3 == None and arg4 == None or arg5 == None:
                    await ctx.send("< Missing Information")

                elif is_maincat(arg3) != True and is_subcat(arg3) != True:
                    await ctx.send("> Category not Found")


                elif is_item(arg3) != True and arg4 in item_types and count == True:
                    #.edit item add (category) dye (dye number)

                    if arg4 == "dye":
                        try:
                            num = int(arg5)
                        except:
                            num = None
                            await ctx.send("> Please enter a valid number")
                        if num == None or isinstance(num, int) == False:
                            await ctx.send(f"> {ctx.prefix}edit item add (category) dye (dye number)")

                        else:
                            collection.insert_one({"type": "dye",
                                                   "under": arg3,
                                                   "name": arg5,
                                                   })
                            dye = db["Dye"]
                            dye.insert_one({"name": arg5,
                                            "bow": {"part A":1, "part B":1, "part C":1},
                                            "OHS": {"part A": 1, "part B": 1, "part C": 1},
                                            "THS": {"part A": 1, "part B": 1, "part C": 1},
                                            "staff": {"part A": 1, "part B": 1, "part C": 1},
                                            "katana": {"part A": 1, "part B": 1, "part C": 1},
                                            "bowgun": {"part A": 1, "part B": 1, "part C": 1},
                                            "halberd": {"part A": 1, "part B": 1, "part C": 1},
                                            "knuckles": {"part A": 1, "part B": 1, "part C": 1},
                                            "MD": {"part A": 1, "part B": 1, "part C": 1},
                                            "armour": {"part A":1, "part B":1, "part C":1},
                                            "additional": {"part A":1, "part B":1, "part C":1},
                                            "edited on": ""
                                            })
                            await ctx.send(f"> Added **Dye {arg5}**")


                    else:
                        collection.insert_one({"type": "item", "under": arg3, "name": arg5})

                        name = metaphone(arg5)
                        print(name)
                        collection2 = db["Items"]
                        collection3 = db["Var"]

                        item = collection3.find_one({"_id": 0})
                        item = item[arg4]
                        collection2.insert_one(
                            {"item type": item,
                             "item_type2": arg4,
                             "under": arg3,
                             "name": arg5,
                             "price": 1,
                             "edited by": "",
                             "edited on": "",
                             "search id": name,
                             }
                        )

                        await ctx.send(f"> Added **{arg5}** in **{arg3}**")
                # elif count == True:
                # await ctx.send("> Duplicate Category Found")

                elif arg4 not in item_types:
                    await item_type(ctx)

                elif count != True:
                    await ctx.send("> Duplicate Item Found")



            # .edit item delete (name)
            elif arg2 == "delete" and arg3 != None and await owner(ctx):
                arg = [arg3, arg4, arg5]
                args = []
                for x in arg:
                    if x != None:
                        args.append(x)
                    else:
                        break
                arg3 = ' '.join(args)
                print(arg3)
                if is_item(arg3) == True:
                    look = collection.find_one({"name": arg3})
                    collection.delete_one(look)
                    collection2 = db["Items"]

                    look2 = collection2.find_one({"name": arg3})
                    collection2.delete_one(look2)
                    await ctx.send(f"> Deleted **{arg3}**")
                #.edit item delete dye (number)
                elif arg3 == "dye" and is_dye(arg4) == True:
                    collection.delete_one({"name":arg4})
                    delete_dye(arg4)
                    await ctx.send(f"> Deleted **{arg3}**")
                else:
                    await ctx.send("> Couldn't delete Item")

            else:
                await ctx.send("> Invalid Command")

        # .edit rename (category/item name)
        elif arg1 == "rename" and arg2 != None:
            arg = [arg2, arg3, arg4, arg5]
            args = []
            for x in arg:
                if x != None:
                    args.append(x)
                else:
                    break
            arg3 = ' '.join(args)
            count = collection.count_documents({"name": arg3})
            if count != 1:
                await ctx.send("> Could not find category/item")
            else:
                send = await ctx.send("> Please input new name...")
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
                        collection.update({"name": arg3},
                                              {"$set":
                                                   {"name": msg.content}
                                               }
                                              )
                        collection2 = db["Items"]
                        count2 = collection2.count_documents({"name": arg3})
                        print(count2)
                        if count2 == 1:
                            collection2.update_one({"name": arg3},
                                                   {"$set":
                                                        {"name": msg.content,
                                                         "search id": metaphone(msg.content)
                                                         }
                                                    }
                                                   )
                        else:
                            print("Work")
                            under = collection.find({"under": arg3})
                            under_items = collection2.find({"under": arg3})
                            for (cat, items) in zips(under, under_items):
                                print(cat, items)
                                if cat != None:
                                    collection.update_one({"_id": cat["_id"]},
                                                          {"$set":
                                                               {"under": msg.content}
                                                           }
                                                          )
                                else:
                                    pass

                                if items != None:
                                    collection2.update_one({"_id": items["_id"]},
                                                          {"$set":
                                                               {"under": msg.content}
                                                           }
                                                          )
                                else:
                                    pass




                        await ctx.send(f"**{arg3}** changed to **{msg.content}**")

                except asyncio.TimeoutError:
                    await send.delete()
                    await ctx.send("> Cancelling...", delete_after=10)







        #.edit link (item name)
        elif arg1 == "link" and await owner(ctx):
            arg3 = [arg3, arg4, arg5]
            args = []
            for x in arg3:
                if x != None:
                    args.append(x)
                else:
                    break
            arg3 = ' '.join(args)
            count = collection.count_documents({"name":arg3})
            count2 = collection.count_documents({"name":arg2})
            if count == 1 and count2 == 1:
                collection.update_one({"name":arg3}, {"$push": {"link":arg2}})
                await ctx.send(f"> Linked **{arg3}** in **{arg2}**")
            else:
                await ctx.send("> Could not Find Arguments")



        elif arg1 == "unlink" and await owner(ctx):
            arg3 = [arg3, arg4, arg5]
            args = []
            for x in arg3:
                if x != None:
                    args.append(x)
                else:
                    break
            arg3 = ' '.join(args)
            count = collection.count_documents({"name": arg3})
            count2 = collection.count_documents({"name": arg2})
            if count == 1 and count2 == 1:
                collection.update_one({"name": arg3}, {"$pull": {"link": arg2}})
                await ctx.send(f"> Unlinked **{arg3}** in **{arg2}**")
            else:
                await ctx.send("> Could not Find Arguments")



        else:
            await ctx.send("> Command not Found")





def setup(bot):
    bot.add_cog(editing(bot))