import sys
import re

from tld import get_tld
import linkGrabber

def get_links(url):
    links = linkGrabber.Links(url)
    for link in links.find():
        curr_link = link['href']

        if curr_link == url:
            continue
        if curr_link in scanned_links:
            continue
        if curr_link in external_links:
            continue
        if is_blacklisted(curr_link):
            continue

        if re.search(domain, curr_link):
            print "Scanning page: %s" % curr_link
            scanned_links.append(curr_link)
            get_links(curr_link)
        else:
            print "Found: %s" % curr_link
            external_links.append(curr_link)

def is_blacklisted(url):
    for item in blacklist:
        if re.search(item, url):
            return True
    return False

if __name__ == '__main__':
    if not sys.argv[1]:
        raise KeyError("First argument should be URL")

    scanned_links = [sys.argv[1]]
    external_links = []
    blacklist = [".pdf", ".jpg", ".jpeg", ".png", ".gif"]
    domain = get_tld(sys.argv[1])

    get_links(sys.argv[1])

    print "Total pages scanned: %s" % len(scanned_links)
    print "Total external links found: %s" % len(external_links)

    if sys.argv[2]:
        with open(sys.argv[2], "w") as fp:
            fp.write("Scanned\n--------------------\n")
            for link in scanned_links:
                fp.write(link + "\n")
            fp.write("\nFound\n--------------------\n")
            for link in external_links:
                fp.write(link + "\n")
            fp.write("\n--------------------\n")
            fp.write("Total pages scanned: %s\n" % len(scanned_links))
            fp.write("Total external links found: %s" % len(external_links))
