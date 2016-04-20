from LocalMiner import LocalMiner
from RemoteMiner import RemoteMiner
from argparse import ArgumentParser
from os import path, makedirs, chdir

status = ['open', 'merged', 'abandoned']


def download_data(args):
    print("Gerrit domains to download data:")

    for arg in args:
        print('\t' + arg)

    print()

    for arg in args:
        domain_split = arg.split('//')[1]

        if not path.exists(domain_split):
            makedirs(domain_split)

        chdir(domain_split)

        for stat in status:
            print("Downloading data of " + stat + " reviews from " + arg)
            LocalMiner(arg, stat)

        chdir('../')


def mine_local(args):
    print(args)


def mine_remote(args):
    print(args)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--local', metavar='l', nargs='+', type=str, help='mine local data from domains list')
    parser.add_argument('--remote', metavar='r', nargs='+', type=str, help='mine remote data from domains list')
    parser.add_argument('--download', metavar='d', nargs='+', type=str, help='download data from domains list')

    args = parser.parse_args()

    if args.local:
        mine_local(args.local)
    elif args.remote:
        mine_remote(args.remote)
    elif args.download:
        download_data(args.download)
