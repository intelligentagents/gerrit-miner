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
                response = loads(request.text[5:])
            else:
                print('Error')

    @staticmethod
    def mine_details(commit, domain):
        details = ['/detail?O=10004']

        for detail in details:
            url = domain + "changes/" + str(commit) + detail
            request = get(url)

            if request.status_code == 200:
                response = loads(request.text[5:])
            else:
                print("Error")

    def mine_review(self, commit, current_revision, domain):
        self.mine_details(commit, domain)
        self.mine_revisions(commit, current_revision, domain)

    @staticmethod
    def search_vccs_in_comments(base_url, keywords_json, commit, domain):
        # URL to comments of a commit
        url = base_url + "/comments"

        # Request the JSON file of this URL
        request = get(url)

        # If request was successful, look for keywords in comments
        if request.status_code == 200:
            response = loads(request.text[5:])
            keys = response.keys()

            for key in keys:
                for comment in response[key]:
                    for keywords in keywords_json['keywords']:
                        if keywords['keyword'] in comment['message']:
                            if keywords['depends_on']:
                                for dependency in keywords['depends_on']:
                                    if dependency in comment['message']:
                                        print("  Found keyword: " + "\033[1m" + keywords['keyword'] + "\033[0m" +
                                              " and the dependency: " + "\033[1m" + dependency + "\033[0m" +
                                              " in comment\n" + "    Domain: " + domain + "\n" + "    Commit: " +
                                              str(commit) + "\n" + "    File: " + key + "\n" + "    Comment ID: " +
                                              comment['id'])
                            else:
                                print("  Found keyword: " + "\033[1m" + keywords['keyword'] + "\033[0m" +
                                      " in comment\n" + "    Domain: " + domain + "\n" + "    Commit: " +
                                      str(commit) + "\n" + "    File: " + key + "\n" + "    Comment ID: " +
                                      comment['id'])

    @staticmethod
    def search_vccs_in_messages(base_url, keywords_json, commit, domain):
        # URL to details of a commit
        url = base_url + "/detail?O=10004"

        # Request the JSON file of this URL
        request = get(url)

        # If request was successful, look for keywords in messages
        if request.status_code == 200:
            response = loads(request.text[5:])

            for message in response['messages']:
                for keywords in keywords_json['keywords']:
                    if keywords['keyword'] in message['message']:
                        if keywords['depends_on']:
                            for dependency in keywords['depends_on']:
                                if dependency in message['message']:
                                    subject = response['subject']

                                    print("  Found keyword: " + "\033[1m" + keywords['keyword'] + "\033[0m" +
                                          " in message\n" + "    Domain: " + domain + "\n" + "    Commit: " +
                                          str(commit) + "\n" + "    Subject: " + subject + "\n" + "    Message ID: " +
                                          message['id'])
        else:
            print("Error")

    def search_vccs(self, commit, domain):
        # Base URL for requests
        base_url = domain + "changes/" + str(commit)

        with open('data/keywords.json') as keywords_file:
            keywords_json = load(keywords_file)

        self.search_vccs_in_messages(base_url, keywords_json, commit, domain)
        self.search_vccs_in_comments(base_url, keywords_json, commit, domain)

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
