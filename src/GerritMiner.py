from Miner import Miner

if __name__ == '__main__':
    domains = ['https://android-review.googlesource.com/', 'https://gerrit.chromium.org/gerrit/']
    status = ['open', 'merged', 'abandoned']

    print("Gerrit URLs to mine:")

    for domain in domains:
        print("\t" + domain)

    print()

    for domain in domains:
        for stat in status:
            print("Mining " + stat + " reviews from " + domain )
            Miner(domain, stat)
