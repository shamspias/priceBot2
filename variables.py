from pymongo import MongoClient
from time import sleep
from datetime import datetime, timedelta
from pytz import timezone
import pytz
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M %Z%z'
times = datetime.utcnow()
now = f"{times.strftime(fmt)}UTC"

pending = dict()


editor = 740103471834857565
moderator = 740167326682316880
server = 740103151767650315
Scroll = "https://cdn.discordapp.com/attachments/432408793998163968/740200163330621450/20200804_185612.jpg"
Coin = "https://cdn.discordapp.com/attachments/432408793998163968/739821516706938980/677105538571567105.png"
Info = "https://cdn.discordapp.com/attachments/748067714722955275/750223872111935519/1598428803482.png"
Monocle = "https://cdn.discordapp.com/attachments/432408793998163968/787508055410868269/1607826945317.png"

Bronze = "<:bronze:788957678415511572>"
Silver = "<:silver:788957718492610570>"
Gold = "<:gold:788957796682563604>"

left = "<:left:790465397232631839>"
right = "<:right:790464686830780468>"

one = "1️⃣"
two = "2️⃣"
three = "3️⃣"
four = "4️⃣"
five = "5️⃣"

item_types = ["staff", "knuckles", "OHS", "THS", "halberd", "MD", "katana", "bow", "bowgun",
              "armour", "additional", "ring", "shield",
              "metal", "wood", "medicine", "cloth", "beast", "mana",
              "potion", "chest", "piercer", "dye", "gems", "powder", "book", "service",
              "special_crysta", "normal_crysta", "armour_crysta", "weapon_crysta", "additional_crysta", "upgrade_crysta"]



