from requests import get
from json import loads


class Miner:
    def __init__(self, domain, stat):
        self.mine(domain, stat)

    @staticmethod
    def mine_revisions(number, current_revision, domain):
        revisions = ['/files']

        for revision in revisions:
            url = domain + "changes/" + str(number) + "/revisions/" + str(current_revision) + revision
            request = get(url)

            if request.status_code == 200:
                return loads(request.text[5:])
            else:
                print("Error")
                return -1

    @staticmethod
    def mine_details(number, domain):
        details = ['/detail?O=10004']
        keywords = ['buffer', 'overflow', 'stack', 'format', 'string','printf', 'scanf', 'integer', 'overflow', \
                    'signedness', 'widthness', 'underflow', 'SQL', 'SQLI', 'injection', 'race', 'racy', 'deadlock', \
                    'improper', 'unauthenticated', 'gain access', 'permission', 'denial service', 'DOS', 'cross site', \
                    'request forgery', 'CSRF', 'XSRF', 'forged', 'security', 'vulnerability', 'vulnerable', 'hole', \
                    'exploit', 'attack', 'bypass', 'backdoor', 'crash', 'threat', 'expose', 'breach', 'violate', \
                    'blacklist', 'overrun', 'insecure']

        for detail in details:
            url = domain + "changes/" + str(number) + detail
            request = get(url)

            if request.status_code == 200:
                response = loads(request.text[5:])
                messages = response['messages']

                message = ",".join(str(m) for m in messages)
                subject = response['subject']

                for keyword in keywords:
                    if keyword in message:
                        print("  Found keyword: " + keyword + ". Stopping to search ...\n" + "    Domain: " + domain + "\n" + "    Commit: " + \
                              str(number) + "\n" + "    Subject: " + subject)
                        break
            else:
                print("Error")

    def mine_reviews(self, number, domain):

        self.mine_details(number, domain)

    def mine(self, domain, status):
        k = 0

        while k <= 9999:
            url = domain + "changes/?q=status:" + status + "&n=100&O=81&S=" + str(k)
            request = get(url)

            if request.status_code == 200:
                reviews = loads(request.text[5:])

                for review in reviews:
                    self.mine_reviews(review['_number'], domain)

                print("")

            k += 100
