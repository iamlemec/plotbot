import sys
import random
import socket
import json
import toml

conf = toml.load(open('conf.toml'))

rand_hex = lambda: hex(random.getrandbits(128))[2:].zfill(32)

def send_file(path, message='', server=conf['server'], channel='general'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((conf['ip'], conf['port']))
    spec = json.dumps({
        'path': path, 'message': message,
        'server': server, 'channel': channel
    })
    data = spec.encode()
    s.sendall(data)

def send_mpl(fig, message='', ext='png', save_args={}, **kwargs):
    tmp_dir = conf['temp_dir']
    tmp_hex = rand_hex()
    tmp_path = f'{tmp_dir}/plotbot_{tmp_hex}.{ext}'
    fig.savefig(tmp_path, **save_args)
    send_file(tmp_path, message=message, **kwargs)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract binned data on visits.')
    parser.add_argument('path', type=str, help='Path to input file')
    parser.add_argument('--message', type=str, default='', help='Text message to send')
    parser.add_argument('--server', type=str, default=conf['server'], help='Server to send to')
    parser.add_argument('--channel', type=str, default='general', help='Channel to send to')
    args = parser.parse_args()

    send_file(args.path, args.message, args.server, args.channel)
