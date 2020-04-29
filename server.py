import os
import json
import toml
import asyncio
import discord

auth = toml.load(open('auth.toml'))
conf = toml.load(open('conf.toml'))

client = discord.Client()
channels = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('We are a member of the following guilds:')
    for g in client.guilds:
        print(g.name)
        for c in g.channels:
            if type(c) is discord.TextChannel:
                print(c.name)
                channels.append((g, c))

@client.event
async def on_message(ctx):
    if 'hello plotbot' in str(ctx.content.lower()):
        await ctx.channel.send('hello!')

async def handle_input(reader, writer):
    data = await reader.read()
    spec = json.loads(data.decode())
    path, mess, serv, chan = spec['path'], spec['message'], spec['server'], spec['channel']
    print(f'{path} ({mess}) ➜ {serv} #{chan}')

    if not os.path.isfile(path):
        print('File not found!')
    fdir, fname = os.path.split(path)
    if len(mess) == 0:
        mess = fname

    for g, c in channels:
        if g.name == serv and c.name == chan:
            with open(path, 'rb') as fid:
                file = discord.File(fid)
                await c.send(mess, file=file)

    writer.close()

async def main():
    await asyncio.gather(
        client.start(auth['token']),
        asyncio.start_server(handle_input, conf['ip'], conf['port'])
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
