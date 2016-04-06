from requests import get
from json import loads


class Miner:
    def __init__(self, domain, stat):
        self.mine(domain, stat)

    def mine_revisions(self, number, current_revision, domain):
        revisions = ['/commit?links', '/related', '/actions', '/files']

        for revision in revisions:
            url = domain + "changes/" + str(number) + "/revisions/" + str(current_revision) + revision
            request = get(url)

            if request.status_code == 200:
                print("    " + url + " - Mined")
                response = loads(request.text[5:])
            else:
                print("Error")

    def mine_details(self, number, domain):
        details = ['/comments', '/submitted_together', '/detail?O=10004']

        for detail in details:
            url = domain + "changes/" + str(number) + detail
            request = get(url)

            if request.status_code == 200:
                print("    " + url + " - Mined")
                response = loads(request.text[5:])

                if detail == "/detail?O=10004":
                    self.mine_revisions(number, response['current_revision'], domain)
            else:
                print("Error")

    def mine_reviews(self, number, domain):
        print("  Mining commit " + str(number))

        self.mine_details(number, domain)


    def mine(self, domain, status):
        k = 0

        while k < 100:
            url = domain + "changes/?q=status:" + status + "&n=100&O=81&S=" + str(k)
            request = get(url)

            if request.status_code == 200:
                reviews = loads(request.text[5:])

                for review in reviews:
                    self.mine_reviews(review['_number'], domain)

                print("")

            k += 100
