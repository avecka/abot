import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import datetime
import time
from flask import Flask
from threading import Thread
import youtube_dl
import requests
import json
import os
from discord.utils import get
from discord import FFmpegPCMAudio
import certifi
import re
from discord.utils import get
import logging
import psycopg2
from mcrcon import MCRcon
import math

app = Flask('')
client = discord.Client()

def run():
  app.run(host='0.0.0.0',port=8080)

@app.route('/',methods=["HEAD","GET"])
def home():
  keep_alive()
  return "cool"

bot = commands.Bot(command_prefix='#', status=discord.Status.dnd, activity=discord.Game(name="Možné chyby.. zkus #abot"))

@bot.event
async def on_ready():
    print ("hello")
    print ("I am running on " + bot.user.name)

    listen_list = ["#abot", "#abot", "#abot", "#abot", "#abot", "#abot", "#abot", "#abot", "twitch.tv/adyas_", "abot2.webnode.cz", "CREATOR: adyas#2815", "ADYASOVO REPUBLIKA", "ADYASOVO REPUBLIKA", "ADYASOVO REPUBLIKA", "ADYASOVO REPUBLIKA", "ADYASOVO REPUBLIKA", "ADYASOVO REPUBLIKA", "Napiš adyasovi o reklamu", "DEJWOSKARMY", "Franťákov"]
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=random.choice(listen_list), type=1))
        await asyncio.sleep(6)


@bot.event
async def on_reaction_add(reaction, user):
  channel = reaction.message.channel
  await bot.send(channel, "{}".format(reaction.emoji))

bot.remove_command("help")

players = {}

@bot.event
async def on_message(message):
        await bot.process_commands(message)

@bot.command()
async def pomoc(ctx):
    await ctx.send("ADMINI **NĚJAKEJ HRÁČ VÁS POTŘEBUJE**")
    print ("user has want help")

@bot.command()
async def dejwoskarmy(ctx):
    embed = discord.Embed(title="Pravidla", description="...", color=0x2fe800)
    embed.add_field(name=".", value="1. Zbytečně nenarušovat hovory.", inline=True)
    embed.add_field(name=".", value="2. Nenadávat si navzájem", inline=True)
    embed.add_field(name=".", value="3. Nezveřejnovat soukromé věci, když daný člověk nechce", inline=True)
    embed.add_field(name=".", value="4. Spam zakázán", inline=True)
    embed.add_field(name=".", value="5. Invity na jiné servery, vaše weby atd.  pouze do #reklamy a pozvánky do her pouze do #pozvánky-lidí-do-hery", inline=True)
    embed.add_field(name=".", value="6. Zakázáno posílání erotických fotek, ... (prostě 18+)", inline=True)
    embed.add_field(name=".", value="7. Admini, kteří chtějí vytvářet a odstranovat roomky, role, atd. , musí si o to zažádat u nejvyšší role na serveru", inline=True)
    embed.add_field(name=".", value="8. Nedávat kontent na jiné # než na které je to určeno např. roblox na #fortnite", inline=True)
    embed.add_field(name=".", value="9. Zbytečně neprosit o lepší roli za nic", inline=True)
    embed.add_field(name=".", value="10. Nepřesouvat uživatele neustále", inline=True)
    embed.add_field(name=".", value="11. Do kategorie historie je zakázáno psát cokoliv, pokud máte právo psát do toho", inline=True)
    embed.add_field(name=".", value="12. Zakázáno měnit přezdívky bez povolení nejvyšší role na serveru", inline=True)
    embed.add_field(name=".", value="13. Zakázáno dávat někomu větší roli než stráž boží, bez povolení nejvyšší role serveru", inline=True)
    embed.add_field(name=".", value="14. @ABOT je povolen skoro na všech textových kanálech, ale nemáte povolení psát třeba do #fortnite #reklama , prostě dané příkazy pište jen, kam se hodí. Blbosti do #příkazy-abot, mapy do svých roomek na hry nebo taky do #příkazy-abot, memes, dances a echo je povoleno ve všech roomkách", inline=True)
    embed.set_footer(text=".")
    await ctx.send(embed=embed)
    print ("user has want help")

#Bot member login
@bot.command() 
async def on_member_join(member):
    print(f'{member} se přidal do party.')

#Bot member logout
@bot.command()
async def on_member_remove(member):
    print(f'{member} nás opustil.')

@bot.command()
async def test(ctx):
	await ctx.send('Obláčky jsou modré a nebe bílé')

@bot.command()
async def sečti(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def odečti(ctx, a: int, b: int):
    await ctx.send(a-b)

@bot.command()
async def vyděl(ctx, a: int, b: int):
    await ctx.send(a/b)

@bot.command()
async def vynásob(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(ctx.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@bot.command(pass_context = True)
async def servers(ctx):
  servers = list(ctx.servers)
  await ctx.sand(f"Connected on {str(len(servers))} servers:")
  await bot.send('\n'.join(server.name for server in servers))

@bot.command()
async def admini(ctx):
    await ctx.send("Koukni do tabulky...")
    print ("admin team")

@bot.command()
async def odpočet(ctx):
    await ctx.message.delete()
    await ctx.send("10", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("9", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("8", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("7", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("6", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("5", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("4", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("3", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("2", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("1", delete_after=2)
    await asyncio.sleep(1)
    await ctx.send("hotovo", delete_after=5)
    print ("odpočet")

@bot.command()
async def minuta(ctx):
    await ctx.message.delete()
    await ctx.send("60", delete_after=10)
    await asyncio.sleep(10)
    await ctx.send("50", delete_after=10)
    await asyncio.sleep(10)
    await ctx.send("40", delete_after=10)
    await asyncio.sleep(10)
    await ctx.send("30", delete_after=10)
    await asyncio.sleep(10)
    await ctx.send("20", delete_after=10)
    await asyncio.sleep(10)
    await ctx.send("10", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("9", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("8", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("7", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("6", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("5", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("4", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("3", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("2", delete_after=1)
    await asyncio.sleep(1)
    await ctx.send("1", delete_after=2)
    await asyncio.sleep(1)
    await ctx.send("hotovo", delete_after=5)
    print ("odpočet")

@bot.command(pass_context=True)
async def server(ctx):
    embed = discord.Embed(name="'s info".format(ctx.message.guild.name), description=ctx.guild.name, color=0x00ff00)
    embed.set_author(name="Server Info")
    embed.add_field(name="Stvořitel", value=ctx.message.guild.owner, inline=True)
    embed.add_field(name="Region", value=ctx.message.guild.region, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.set_footer(text=f'Příkaz napsal {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f'Info o - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Příkaz napsal {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='Jméno na serveru:', value=member.display_name)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name='účet stvořen:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

    embed.add_field(name=f'role ({len(roles)})', value=' '.join([role.mention for role in roles]))
    embed.add_field(name='Nejvyšší role:', value=member.top_role.mention)

    embed.add_field(name='Je to bot?', value=member.bot)
    await ctx.send(embed=embed)
    await asyncio.sleep(10)
    await ctx.message.delete()

@bot.command(pass_context=True)
@commands.has_role("clear")
async def clear(ctx, amount=100):
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(description="Smazáno! :smile:", color=0x00ff00)
    await ctx.send(embed=embed, delete_after=5)

@bot.command(pass_context=True)
@commands.has_role("Správce boží vůle")
async def klír(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(description="Smazáno! :smile:", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("KOKOT-strike")
async def klear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(description="Smazáno! :smile:", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
async def kaprsnivou(ctx):
    await ctx.send("https://www.youtube.com/watch?v=u1ZZ85DOL6w")
    print ("kaprsnivou")

@bot.command()
async def chcípáci(ctx):
    await ctx.send("https://www.youtube.com/watch?v=pnvYGhoYPYQ")
    print ("kaprsnivou")

@bot.command(pass_context=True)
@commands.has_role("PREZIDENT")
async def ban(ctx, member : discord.Member):
    role = get(member.guild.roles, name="BANNUT")
    await member.add_roles(member, role)
    embed = discord.Embed(description="Panečku ten tě asi naštval co že si mu dal ban! :smile:", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("PREZIDENT")
async def jsemadmin(ctx):
    await ctx.send("ano jsi")

@bot.command()
async def eventor(ctx):
    await ctx.send("**__Dejwosk__**")
    print ("eventor")

@bot.command()
async def ncs(ctx):
    await ctx.send("!play ncs")
    print ("ncs")

@bot.command()
async def jatrovyknedlicek(ctx):
    await ctx.send("https://www.youtube.com/watch?v=MPX71YiUYTc")
    print ("ncs")

@bot.command()
async def dort(ctx):
    await ctx.send(":dortiksjahodami:")
    print ("ncs")

@bot.command()
async def abot(ctx):
    await ctx.send("**#pomoc  #verze  #userinfo [@název hráče]  #ping  #admini  #eventor  #creator  #event  #achjo   #status   #server   #čus   #apple   #fortmap   #lolmap   #gta5map   #gif   #rdance   #pubgmap   #overeno   #coin   #echo   #support   #kolikje   #word   #emoji   #praha   #Liptovský_Mikuláš    #coříkáš   #Dejwoskarmy   #jatrovyknedlicek   #pal   #russianroulette  #kaprsnivou   #chcípáci   #vánoce   #odpočet   #ohodnoť   #sečti   #vynásob   #odečti   #vyděl   #minuta**")
    print ("commandy")

@bot.command()
async def verze(ctx):
    await ctx.send("jsem ve verzi 5.4")
    print ("ncs")

@bot.command()
async def achjo(ctx):
    await ctx.send("**hmm**")
    print ("ach jo")

@bot.command()
async def status(ctx):
    await ctx.send("**Hele adyas na mě pracuje tak občas na něco neodpovím ale zkoušej to. Ale ale když už adyas pracuje tak mu napiš super věc a on jí možná přidá {}**".format(ctx.message.author.mention))
    print ("online")

@bot.command()
async def creator(ctx):
    embed = discord.Embed(title="Creator", description="adyas#2815", color=0x2fe800)
    embed.add_field(name="Main server", value="Adyasovo Republika", inline=True)
    embed.set_image(url="https://cdn.discordapp.com/attachments/519518161935138847/644531652718100480/20191114_143609.gif")
    embed.set_footer(text="_____________________________________________________")
    embed.add_field(name="Link", value="https://discord.gg/MdYqaMS", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def scrt(ctx):
    await ctx.send("**end")
    print ("secreet")

@bot.command()
async def event(ctx):
    await ctx.send("**Vše na dejwoskarmy**")
    print ("event")

@bot.command()
async def čus(ctx):
    await ctx.send("Nazdar {} co chceš".format(ctx.message.author.mention))
    print ("ahoj")

@bot.command()
async def nic(ctx):
    await ctx.send("Ach jo tak příště xd")
    print ("nic")

@bot.command()
async def vánoce(ctx):
    await ctx.send("https://yourchristmascountdown.com/")

@bot.command()
async def apple(ctx):
    await ctx.send("https://cdn.vox-cdn.com/thumbor/-bKrYahnwqww9sH9v2h34v9ViA0=/0x114:585x559/1200x800/filters:focal(248x297:340x389)/cdn.vox-cdn.com/uploads/chorus_image/image/57272301/Screen_Shot_2017_10_23_at_10.16.32_AM.0.png")


@bot.command()
async def fortmap(ctx):
    await ctx.send("https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwiYlrnX7IzkAhUCbFAKHYijDtgQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.gamespot.com%2Farticles%2Fhow-fortnites-map-has-changed-in-season-10-rift-zo%2F1100-6468827%2F&psig=AOvVaw2N7rY6Y270Wo1MPFjbxoHM&ust=1566232447712676")

@bot.command()
async def lolmap(ctx):
    await ctx.send("http://www.lolko.estranky.cz/img/mid/1/league-of-legends-map.jpg")

@bot.command()
async def gta5map(ctx):
    await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQctCYy0Zi5AAWyaYieC9xTnKKY9-nEbqli12HkR98QKZRLrNa_")

@bot.command()
async def gif(ctx):
    await ctx.send("https://giphy.com/explore/random")

@bot.command()
async def rdance(ctx):
    await ctx.send("https://media.discordapp.net/attachments/518083878817234944/531040356217651200/ds_rainbow_dance.gif?width=84&height=84")

@bot.command()
async def pubgmap(ctx):
    await ctx.send("https://d1nglqw9e0mrau.cloudfront.net/assets/images/thumbs/erangel-ee673d73.jpg")

@bot.command()
async def car(ctx):
    await ctx.send("https://m.static.lagardere.cz/frekvence1/edee/clanky/21980/trabant.jpg")

@bot.command()
async def overeno(ctx):
    await ctx.send("Tento server je ověřen mnou")

@bot.command(pass_context = True)
async def coin(ctx):
    await ctx.send(random.randint(1,101))

@bot.command(pass_context = True)
async def ohodnoť(ctx):
    await ctx.send(random.randint(0,10))

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def support(ctx):
    await ctx.send("**https://discord.gg/Q2kXk7K**")
    print ("server abotovo")

@bot.command(pass_context = True)
async def tonido(ctx):
    await ctx.send(random.randint(20,58))
    await ctx.send("cpu% ")
    await ctx.send(random.randint(40,60))
    await ctx.send("ram% ")
    await ctx.send(random.randint(60,90))
    await ctx.send("gpu% ")

@bot.command()
async def btc(currency : str):
    """fetches bitcoin price."""
    url = 'https://blockchain.info/ticker'
    resp = requests.get(url)
    btc = resp.json()[currency]
    await bot.say(btc['symbol'] + ' ' + str(btc['last']))

@bot.command()
async def srvr(ctx):
    await ctx.send("**Ověřování**")
    await ctx.send("**0%**")
    await ctx.send("**39%**")
    await ctx.send("**68%**")
    await ctx.send("**99%**")
    await ctx.send("**Ověřeno {}**".format(ctx.message.author.mention))
    print ("server overeni")

@bot.command()
async def kolikje(ctx):
    await ctx.send("dneska je")
    await ctx.send(datetime.datetime.today());
    await ctx.send("{}".format(ctx.message.author.mention))
    print ("hodiny")

@bot.command()
async def word(ctx):
    word = ["ahoj", "doháje", "server", "python", "lucky", "dgdfhfgchfd", "nic víc", "ukousnu ti nohu", "kurvajčkasnáší", "jajajajaja", "discord", "asi si prohrál lol", "lalala abotla lalala", "hudbička", "co se dá dělat", "kámo já uź fakt nevím co mám říct tyvole máš tady echo a používáš milion let starej příkaz ale okej"]
    await ctx.send(random.choice(word))
    print ("word")  

@bot.command()
async def russianroulette(ctx):
    word = ["tady hajzle más 1strike", "tady máš dárek v podobě 1 sriku", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "dostáváš hovno", "kod:je použit"]
    await ctx.send(random.choice(word))
    print ("ruská ruleta")  


@bot.command()
async def emoji(ctx):
    word = [":cookie:", ":thumbsup:", ":thumbsdown:", ":sneezing_face:", ":call_me:", ":full_moon_with_face:", ":robot:", ":hamburger:", ":poop:", ":rage:", ":popcorn:", ":8ball:", ":watch"]
    await ctx.send(random.choice(word))
    print ("emoji") 

@bot.command()
async def coříkáš(ctx):
    word = ["je to ok", "dobře", "to by dal každej", "no kámo", "najs kamaráde", "jako bylo to dobrý", "lol..."]
    await ctx.send(random.choice(word))
    print ("najs") 

@bot.command()
async def pal(ctx):
    word = ["kámo skoro jsem ho měl", "těsně ale vedle", "půlka dole", "všechno jsem zasáhl", "bouhžel tak dobrej nejsem aby sem se trefil pokaždé ale zkus to znovu", "jednoho z nich mám", "je dole", "co se dá dělat netrefil jsem se", "trefa haha", "muhahahah je to tam"]
    await ctx.send(random.choice(word))
    print ("pálím") 

@bot.command()
async def reklama(ctx):
    word = ["https://adyas.webnode.cz", "Kup si hru dead by daylight https://store.steampowered.com/app/381210/Dead_by_Daylight/", "https://twitch.tv/firden_/", "https://twitch.tv/adyas_/", "https://twitch.tv/adyas_/", "https://twitch.tv/adyas_/" ]
    await ctx.send(random.choice(word))
    print ("reklama") 

@bot.command()
async def praha(ctx):
    await ctx.send("https://meteobox.cz/praha/")

testing = False

@bot.command()
async def testingmode(ctx):
    global testing
    if testing:
        testing = False
        await ctx.send("Testing mode deactivated")
    else:
        testing = True
        await ctx.send("Testing mode activated")

@bot.command()
async def is_staff(ctx):
    for permissionRole in ctx.author.roles:
        if permissionRole.id == int(os.environ['440430041491308544']) or permissionRole.id == int(
                os.environ['440430041491308544']):
            return True

@bot.command()
async def pocasí(ctx):
    await ctx.send("https://meteobox.cz/")

@bot.command()
async def mdfnkl(ctx):
    await ctx.send("bannut")

@bot.command()
async def Liptovský_Mikuláš(ctx):
    await ctx.send("https://meteobox.cz/slovensko/liptovsky-mikulas/")

@bot.command()
async def meme(ctx):
  r = requests.get("https://api.reddit.com/r/memes/hot?limit=100", headers = {'User-agent': 'Discord Bot'})
  res = r.content
  res = json.loads(res)
  post = random.randint(0,int(res["data"]["dist"]) - 1)
  embed=discord.Embed(title=res["data"]["children"][post]["data"]["title"], description="by " + res["data"]["children"][post]["data"]["author"], url="https://reddit.com" + res["data"]["children"][post]["data"]["permalink"])
  embed.set_footer(text="Reddit")
  await ctx.send(ctx.message.channel, embed=embed)

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()

bot.run("token here")


