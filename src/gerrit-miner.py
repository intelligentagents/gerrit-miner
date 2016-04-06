from requests import get
from json import loads


def mine_revisions(number, current_revision, domain):
    revisions = ['/commit?links', '/related', '/actions', '/files']

    for revision in revisions:
        url = domain + "changes/" + str(number) + "/revisions/" + str(current_revision) + revision
        request = get(url)

        if request.status_code == 200:
            print("    " + url + " - Mined")
            response = loads(request.text[5:])
        else:
            print("Error")


def mine_details(number, domain):
    details = ['/comments', '/submitted_together', '/detail?O=10004']

    for detail in details:
        url = domain + "changes/" + str(number) + detail
        request = get(url)

        if request.status_code == 200:
            print("    " + url + " - Mined")
            response = loads(request.text[5:])

            if detail == "/detail?O=10004":
                mine_revisions(number, response['current_revision'], domain)
        else:
            print("Error")


def mine_reviews(number, change_id, domain):
    print("  Mining commit " + str(number))

    mine_details(number, domain)


def mine(domain, status):
    k = 0

    while k < 100:
        url = domain + "changes/?q=status:" + status + "&n=100&O=81&S=" + str(k)
        request = get(url)

        if request.status_code == 200:
            reviews = loads(request.text[5:])

            for review in reviews:
                mine_reviews(review['_number'], review['change_id'], domain)

            print("")

        k += 100

status = ['open', 'merged', 'abandoned']
domains = ['https://android-review.googlesource.com/', 'https://gerrit.chromium.org/gerrit/']

for domain in domains:
    for stat in status:
        print("Mining " + stat + " reviews from " + domain)
        mine(domain, stat)
