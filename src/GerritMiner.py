from src.Miner import Miner

status = ['open', 'merged', 'abandoned']
domains = ['https://android-review.googlesource.com/', 'https://gerrit.chromium.org/gerrit/']

for domain in domains:
    for stat in status:
        print("Mining " + stat + " reviews from " + domain)
        Miner(domain, stat)
