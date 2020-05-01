import os
import json
import toml
import asyncio
import discord

bot_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{bot_dir}/auth.toml') as aid:
    auth = toml.load(aid)
with open(f'{bot_dir}/conf.toml') as cid:
    conf = toml.load(cid)

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
                print(f'#{c.name}')
                channels.append((g, c))

async def send_discord(file, message, server, channel):
    sent = False
    for g, c in channels:
        if g.name == server and c.name == channel:
            await c.send(message, file=file)
            sent = True
    return sent

async def handle_input(reader, writer):
    data = await reader.read(4092)
    spec = json.loads(data.decode())
    path, mess, serv, chan = spec['path'], spec['message'], spec['server'], spec['channel']
    print(f'{path} ({mess}) -> {serv} #{chan}')

    fdir, fname = os.path.split(path)
    if len(mess) == 0:
        mess = fname

    if not os.path.isfile(path):
        sent = False
        stat = 'Not a valid file'
    else:
        with open(path, 'rb') as fid:
            file = discord.File(fid)
            sent = await send_discord(file, mess, serv, chan)
        stat = 'Success' if sent else 'Channel not found'

    res = json.dumps({'sent': sent, 'status': stat})
    writer.write(res.encode())
    await writer.drain()
    writer.close()

async def main():
    await asyncio.gather(
        client.start(auth['token']),
        asyncio.start_server(handle_input, conf['ip'], conf['port'])
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
