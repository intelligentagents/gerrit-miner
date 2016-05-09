from requests import get
from json import loads
from os import path, makedirs, chdir
from time import sleep
from sys import stdout
from datetime import datetime


class Download:
    def __init__(self, domain, stat):
        self.mine(domain, stat)

    def try_connection(self, url):
        # Request the JSON file of this URL
        request = get(url)
        print('\t\tURL: ' + request.url)

        # Save the json in a file or retry connection if blocked
        if request.status_code == 200:
            print('\t\t\tResponse status code: ' + str(request.status_code))
            print('\t\t\tContent Type: ' + request.headers['Content-Type'])

            with open('comments.json', 'wb') as json:
                json.write(request.content)
        elif request.status_code == 429:
            print('\t\t\tResponse status code: ' + str(request.status_code))

            if 'retry-after' in request.headers:
                for remaining in range(int(request.headers['retry-after']), 0, -1):
                    stdout.write("\r")
                    stdout.write("\t\t\t\tConnection failed. {:2d} seconds to retry".format(remaining))
                    stdout.flush()
                    sleep(1)
            else:
                for remaining in range(3600, 0, -1):
                    stdout.write("\r")
                    stdout.write("\t\t\t\tConnection failed. No Retry-After header found. {:2d} seconds to retry".format(remaining))
                    stdout.flush()
                    sleep(1)

            stdout.write("\r\t\t\t\tRetrying ...\n")

            self.try_connection(url)

        return request.status_code

    def download_comments(self, base_url, commit, domain):
        # URL to details of a commit
        url = base_url + "/comments"

        with open('../../log.txt', 'a') as log:
            if self.try_connection(url) == 200:
                log.write('\t' + url + ':\n' + '\t\tStatus code: 200\n' + '\t\tTime: ' + str(datetime.now()) + '\n')
            elif self.try_connection(url) == 429:
                log.write('\t' + url + ':\n' + '\t\tStatus code: 429\n' + '\t\tTime: ' + str(datetime.now()) + '\n')

    def download_details(self, base_url, commit, domain):
        # URL to details of a commit
        url = base_url + "/detail?O=10004"

        with open('../../log.txt', 'a') as log:
            if self.try_connection(url) == 200:
                log.write('\t' + url + ':\n' + '\t\tStatus code: 200\n' + '\t\tTime: ' + str(datetime.now()) + '\n')
            elif self.try_connection(url) == 429:
                log.write('\t' + url + ':\n' + '\t\tStatus code: 429\n' + '\t\tTime: ' + str(datetime.now()) + '\n')

    def download_data(self, commit, domain):
        # Base URL for requests
        base_url = domain + "changes/" + str(commit)

        print('\tChange ID: ' + str(commit))

        with open('../../log.txt', 'a') as log:
            log.write(domain + str(commit) + ':\n')

        self.download_details(base_url, commit, domain)
        self.download_comments(base_url, commit, domain)

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