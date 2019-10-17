import discord
import time
import asyncio
from discord.ext import commands
#from discord.ext import task
from itertools import cycle

messages = joined = 0
status = cycle(['Sziasztok!', 'Hello!', 'Üdv!'])
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()
#client2 = commands.Bot(command_prefix = '!')



async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


#@client.event
#async def on_member_update(before, after):
   # n = after.Kristóf
    #if n:
        #if n.lower().count("Kristóf") > 0:
           # last = before.Kristóf
            #if last:
              #  await after.edit(Kristóf=last)
            #else:
                #await after.edit(Kristóf="STOP")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "általános":
            await channel.send(f"""Üdvözöllek a szerveren! {member.mention} """)


@client.event
async def on_ready():
    change_status.start()
#async def clear(ctx, amount=5):
    #await ctx.channel.purge(limit=amount)
    #joined -= 1
    #for channel in member.server.channels:
        #if str(channel) == "általános":
            #await channel.send(f"Viszlát! {member.mention} ")



#@tasks.loop(second=10)
#async def change_status():
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))
 
    #await member.kick(reason=reason)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Sziasztok!"))
 


@client.event
async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(632883880432762891)
    channels = ["általános"]
    valid_users = ["Kristóf#9857"]
    bad_words = ["hülye", "szar",]

    for word in bad_words:
        if message.content.count(word) > 0:
            print("Tiltott üzenet")
            await message.channel.purge(limit=1)
            await message.channel.send("Ne beszélj csúnyán!") 

    if message.content == "!help":
        embed = discord.Embed(title="BOT parancsok", description="Általános parancsok")
        embed.add_field(name="!hello", value="Üdvözöl")
        embed.add_field(name="!users", value="Tagok")
        await message.channel.send(content=None, embed=embed)

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("!hello") != -1:
            await message.channel.send("Szia!") 
        elif message.content == "!users":
            await message.channel.send(f"""Tagok: {id.member_count}""")


    #if str(message.channel) in channels and str(message.author) in valid_users:
        #if message.content.find("!kick") != -1:
            #async def kick(ctx, member : discord.Member, *, reason=None):
    #await member.kick(reason=reason)

    #if message.content.find (bad_words):
       # await message.channel.send("Ne beszélj csúnyán!") 





client.loop.create_task(update_stats())
client.run(token)