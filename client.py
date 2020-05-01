import os
import random
import json
import toml
import asyncio

bot_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{bot_dir}/conf.toml') as cid:
    conf = toml.load(cid)

rand_hex = lambda: hex(random.getrandbits(128))[2:].zfill(32)

async def send_async(spec):
    reader, writer = await asyncio.open_connection(conf['ip'], conf['port'])
    writer.write(spec.encode())
    ret = await reader.read(1024)
    stat = json.loads(ret.decode())
    writer.close()
    return stat

def send_file(path, server, message='', channel='general'):
    spec = json.dumps({'path': path, 'message': message, 'server': server, 'channel': channel})
    return asyncio.run(send_async(spec))

def send_mpl(fig, server, ext='png', save_args={}, **kwargs):
    tmp_dir = conf['temp_dir']
    tmp_hex = rand_hex()
    tmp_path = f'{tmp_dir}/plotbot_{tmp_hex}.{ext}'

    fig.savefig(tmp_path, **save_args)
    ret = send_file(tmp_path, server, **kwargs)
    os.remove(tmp_path)

    return ret

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract binned data on visits.')
    parser.add_argument('path', type=str, help='Path to input file')
    parser.add_argument('--message', type=str, default='', help='Text message to send')
    parser.add_argument('--server', type=str, default=conf['server'], help='Server to send to')
    parser.add_argument('--channel', type=str, default='general', help='Channel to send to')
    args = parser.parse_args()

    ret = send_file(args.path, args.message, args.server, args.channel)

    print(f'sent   = {ret["sent"]}')
    print(f'status = {ret["status"]}')
