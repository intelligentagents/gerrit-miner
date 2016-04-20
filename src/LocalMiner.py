from requests import get
from json import loads
import urllib
from os import path, makedirs, chdir


class LocalMiner:
    def __init__(self, domain, stat):
        self.mine(domain, stat)

    @staticmethod
    def download_comments(base_url, commit, domain):
        # URL to details of a commit
        url = base_url + "/comments"

        # Request the JSON file of this URL
        urllib.request.urlretrieve(url, 'comments.json')

    @staticmethod
    def download_details(base_url, commit, domain):
        # URL to details of a commit
        url = base_url + "/detail?O=10004"

        # Request the JSON file of this URL
        urllib.request.urlretrieve(url, 'messages.json')

    def download_data(self, commit, domain):
        # Base URL for requests
        base_url = domain + "changes/" + str(commit)

        print('\t' + str(commit) + ': ', end='')

        self.download_details(base_url, commit, domain)
        self.download_comments(base_url, commit, domain)

        print("\033[1m" + u'\u2713' + "\033[0m")

    def mine(self, domain, status):
        i = 0

        if not path.exists(status):
            makedirs(status)

        chdir(status)

        while i <= 9999:
            url = domain + "changes/?q=status:" + status + "&n=100&O=81&S=" + str(i)
            request = get(url)

            if request.status_code == 200:
                reviews = loads(request.text[5:])

                for review in reviews:
                    change_id = review['_number']

                    if not path.exists(change_id):
                        makedirs(str(change_id), exist_ok=True)

                    chdir(str(change_id))

                    self.download_data(change_id, domain)

                    chdir('../')

                print("")

            i += 100

        chdir('../')