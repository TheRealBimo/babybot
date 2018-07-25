import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import youtube_dl
import json
import os

TOKEN = 'Why would I include this :^)'

os.chdir(r'C:\Users\USERNAME\Desktop\baby bot')

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

players = {}
queues = {}

def check_queue(id):
    if queues[id] !=[]:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

status = ['use .help' 'Sleeping in bed', 'Eating baby food', 'Playing with toys', 'Crying! WAAAAAAA!']

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(420)

@client.event
async def on_ready():
    print('Bot is online.')

# Ping Command
@client.command()
async def ping():
    await client.say('Pong!')

# Echo Command
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

# Local Logging
@client.event
async def on_message(message):
    print('A user has sent a message')
    await client.process_commands(message)

# Clear Command
@client.command(pass_context=True)
async def clear(ctx, amount=10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted.')

# Automatic Role
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Member')
    await client.add_roles(member, role)

# Example Embed
@client.command(pass_context=True)
async def displayembed():
    embed = discord.Embed(
        title = 'Title', 
        description = 'This is a description',
        colour = discord.Colour.blue()
    )

    embed.set_footer(text='Baby Bot by Bimo')
    embed.set_image(url='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    embed.set_thumbnail(url ='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    embed.set_author(name='Bimo', 
    icon_url='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    await client.say(embed=embed)


# Info Embed
@client.command()
async def info():
    info = discord.Embed(
        title = 'Baby Bot Information', 
        description = 'This is a cool administrative, server status and music bot',
        colour = discord.Colour.blue()
    )

    info.set_footer(text='Baby Bot by Bimo')
    info.set_image(url='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    info.set_thumbnail(url ='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    info.set_author(name='Bimo', 
    icon_url='https://cdn.discordapp.com/attachments/442779191390371841/471428909091651604/0f837319a39026212f4597d6a57948ce2541dff2_full.jpg.6c856cd0fb9c8c1add975d2f881826b3.jpg')
    info.add_field(name='Field Name', value='Field Value', inline=False)
    info.add_field(name='Field Name', value='Field Value', inline=True)
    info.add_field(name='Field Name', value='Field Value', inline=True)

    await client.say(embed=info)

# Help Commmands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    
    embed.set_footer(text='My first bot by bimo :)')


    embed.set_author(name='Help')
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)
    embed.add_field(name='.clear', value='Deletes messages', inline=False)
    embed.add_field(name='.echo', value='Repeats your message', inline=False)
    embed.add_field(name='.join', value='Bot joins your channel', inline=False)
    embed.add_field(name='.leave', value='Bot leaves your channel', inline=False)
    embed.add_field(name='.play', value='Plays your youtube video', inline=False)
    embed.add_field(name='.pause', value='Pauses the video', inline=False)
    embed.add_field(name='.resume', value='Resumes the video', inline=False)
    embed.add_field(name='.stop', value='Stops the video', inline=False)
    embed.add_field(name='.queue', value='Adds the video to the queue', inline=False)
    embed.add_field(name='.github', value='Download the source code here', inline=False)
    await client.send_message(author, embed=embed)

# Reaction Logger - Added
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

# Reaction Logger - Removed
@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

# Bot join voice channel
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

# Bot leaves voice channel
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

# Play command (Youtube videos) auto joins
@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

# Pause command (music bot)
@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

# Stop command (music bot)
@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

# Resume command (music bot)
@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

# Queues (music bot)
@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video Added.')


client.loop.create_task(change_status())
client.run(TOKEN)
