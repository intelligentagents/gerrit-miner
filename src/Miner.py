from requests import get
from json import loads, load


class Miner:
    def __init__(self, domain, stat):
        self.mine(domain, stat)

    @staticmethod
    def mine_revisions(commit, current_revision, domain):
        revisions = ['/files']

        for revision in revisions:
            url = domain + 'changes/' + str(commit) + '/revisions/' + str(current_revision) + revision
            request = get(url)

            if request.status_code == 200:
                return loads(request.text[5:])
            else:
                print('Error')
                return -1

    @staticmethod
    def mine_details(commit, domain):
        details = ['/detail?O=10004']

        for detail in details:
            url = domain + "changes/" + str(commit) + detail
            request = get(url)

            if request.status_code == 200:
                response = loads(request.text[5:])

                message = ",".join(str(m) for m in response['messages'])
                subject = response['subject']

                for keyword in keywords:
                    if keyword in message:
                        print("  Found keyword: " + keyword + ". Stopping to search ...\n" + "    Domain: " + domain + "\n" + "    Commit: " + \
                              str(commit) + "\n" + "    Subject: " + subject)
                        break
            else:
                print("Error")

    def mine_review(self, commit, current_revision, domain):
        self.mine_details(commit, domain)
        self.mine_revisions(commit, current_revision, domain)

    def search_vccs(self, commit, domain):
        comments_urls = ['/detail?O=10004']

        with open('data/keywords.json') as keywords_file:
            keywords = load(keywords_file)

        for comment_url in comments_urls:
            url = domain + "changes/" + str(commit) + comment_url
            request = get(url)

            if request.status_code == 200:
                response = loads(request.text[5:])

                message = ",".join(str(m) for m in response['messages'])

                for keyword in keywords['keywords']:
                    if keyword in message:
                        subject = response['subject']

                        print("  Found keyword: " + keyword + ". Stopping to search ...\n" + "    Domain: " + domain + "\n" + "    Commit: " + \
                              str(commit) + "\n" + "    Subject: " + subject)
                        break
            else:
                print("Error")

    def mine(self, domain, status):
        k = 0

        while k <= 9999:
            url = domain + "changes/?q=status:" + status + "&n=100&O=81&S=" + str(k)
            request = get(url)

            if request.status_code == 200:
                reviews = loads(request.text[5:])

                for review in reviews:
                    self.search_vccs(review['_number'], domain)

                print("")

            k += 100
