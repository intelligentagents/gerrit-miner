from src.Miner import Miner
from multiprocessing import Process


def mine_android():
    domain = "https://android-review.googlesource.com/"
    status = ['open', 'merged', 'abandoned']

    for stat in status:
        print("Mining " + stat + " reviews from " + "Android")
        Miner(domain, stat)


def mine_chromium():
    domain = "https://gerrit.chromium.org/gerrit/"
    status = ['open', 'merged', 'abandoned']

    for stat in status:
        print("Mining " + stat + " reviews from " + "Chromium")
        Miner(domain, stat)

if __name__ == '__main__':
    process1 = Process(target=mine_android)
    process1.start()

    process2 = Process(target=mine_chromium)
    process2.start()

    process1.join()
    process2.join()