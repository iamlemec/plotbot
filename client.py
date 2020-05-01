import os
import random
import json
import toml
import socket

bot_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{bot_dir}/conf.toml') as cid:
    conf = toml.load(cid)

rand_hex = lambda: hex(random.getrandbits(128))[2:].zfill(32)

def send_sync(spec):
    text = json.dumps(spec).encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((conf['ip'], conf['port']))
        s.sendall(text)
        ret = s.recv(1024)
    stat = json.loads(ret.decode())
    return stat

def send_file(path, server, message='', channel='general'):
    return send_sync({
        'path': path,
        'message': message,
        'server': server,
        'channel': channel
    })

def send_mpl(fig, server, ext='png', save_args={}, **kwargs):
    tmp_dir = conf['temp_dir']
    tmp_hex = rand_hex()
    tmp_path = f'{tmp_dir}/plotbot_{tmp_hex}.{ext}'

    save_args1 = {'bbox_inches': 'tight', 'dpi': 150, **save_args}
    fig.savefig(tmp_path, **save_args1)
    ret = send_file(tmp_path, server, **kwargs)
    os.remove(tmp_path)

    return ret

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract binned data on visits.')
    parser.add_argument('path', type=str, help='Path to input file')
    parser.add_argument('server', type=str, help='Server to send to')
    parser.add_argument('--message', type=str, default='', help='Text message to send')
    parser.add_argument('--channel', type=str, default='general', help='Channel to send to')
    args = parser.parse_args()

    ret = send_file(args.path, args.message, args.server, args.channel)

    print(f'sent   = {ret["sent"]}')
    print(f'status = {ret["status"]}')
