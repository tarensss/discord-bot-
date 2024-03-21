import discord
import youtube_dl
import asyncio
from ctypes.util import find_library
import youtube_dl as yt
from discord import opus
import nacl
import threading
import re
from random import randint
from time import gmtime, strftime
from discord.ext.commands import Bot
import random
from discord import Game
from discord import Emoji, Message
from discord.voice_client import VoiceClient
players = {}
BOT_PREFIX = ("?", "!")
TOKEN = ""
client = Bot(command_prefix=BOT_PREFIX)
#client = discord.Client()
#channel = client.get_channel("")
@client.command(name = 'test', description = 'Only for test purposes', brief = 'Test', pass_context = True)
async def test(ctx):
   possible_responses = [
       'Test', 'Testing', 'Hey', 'Nice'
       ]
   await client.say(random.choice(possible_responses) + " " + ctx.message.author.mention)
@client.command(name = 'kick', description = 'To kick someone', brief = 'Kick', pass_context = True)
async def kick(ctx, member : discord.User, *, reason = None):
    await client.kick(member)
    await client.say("KICKED!")
@client.command(name = 'ban', description = 'To ban someone', brief = 'Ban', pass_context = True)
async def ban(ctx, member : discord.User, *, reason = None):
    await client.ban(member)
    await client.say("BANNED!")
@client.command(name = 'unban', description = 'To unban someone', brief = 'Unban', pass_context = True)
async def unban(ctx, *, member):
    ban_list = await client.get_bans(ctx.message.server)
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
        await client.say("Ban list is empty.")
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say("Unbanned user: `{}`".format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say("I do not have permission to unban.")
        return
    except discord.HTTPException:
        await client.say("Unban failed.")
        return
@client.command(pass_context = True, brief = 'To clear messages')
async def clear(ctx, msglimit : int):
        deleted = await client.purge_from(ctx.message.channel, limit=msglimit)
        await client.say("Cleared **{}** Messages".format(len(deleted)))
@client.command(pass_context = True, brief = 'change nickname')
async def nickname(ctx, member : discord.User, nickname):
    await client.change_nickname(member, nickname)
@client.command(name = "join",pass_context = True)
async def join(ctx):
    channel = client.get_channel("")
    await client.join_voice_channel(channel)

@client.command(name = "check",pass_context = True)
async def check(ctx):
    server = ctx.message.server
    if client.is_voice_connected(server):
        print("Yes")
    else:
        print("No")

@client.command(name = "leave",pass_context = True)
async def leave(ctx):
 channel = client.get_channel("")
 voice_client = client.voice_client_in(channel)
 if voice_client:
        await voice_client.disconnect(channel)
        print("Bot left the voice channel")
 else:
        print("Bot was not in channel")
@client.command(pass_context = True)
async def play(ctx, url):
    channel = client.get_channel("")
    voice = client.join_voice_channel(channel)
    use_avconv = ('use_avconv', False)
    opts = {
            'format': 'webm[abr>0]/bestaudio/best',
            'prefer_ffmpeg': not use_avconv
        }
    player = voice.create_ytdl_player('song url',ytdl_options=opts)
    # ffmpeg player works
    # p = voice.create_ffmpeg_player(player.download_url)
    player.volume = 0.5
    player.start()
    print('playing')
#@client.event
#async def on_member_join(member):
#    server = member.server
#    for user in server.members:
#        if user.server_permissions.administrator:
#          await client.send_message(user, "A new member has joined")
@client.event
async def on_ready():
    await client.change_presence(game=Game(name= "Joker", type=3)) #3 watch - 2 listen - 1 stream - 0 play
    print("-----------------------------------------")
    print("Logged in " + client.user.name)
    print("-----------------------------------------")

        
client.run(TOKEN)
