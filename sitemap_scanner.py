import os
import sys
import re

from tld import get_tld
import linkGrabber

def get_links(url):
    links = linkGrabber.Links(url)
    for link in links.find():
        curr_link = link['href']

        continue_flag = False
        for item in blacklist:
            if re.search(item, curr_link):
                continue_flag = True
                break
        if continue_flag:
            continue

        if (url != curr_link 
            and curr_link not in scanned_links 
            and re.search(domain, curr_link)):
                print "Scanning page: %s" % curr_link
                scanned_links.append(curr_link)
                get_links(curr_link)
        elif (not re.search(domain, curr_link) 
            and curr_link not in external_links):
                print "Found: %s" % curr_link
                external_links.append(curr_link)

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
            fp.write("Found\n--------------------\n")
            for link in external_links:
                fp.write(link + "\n")
            fp.write("--------------------\n")
            fp.write("Total pages scanned: %s\n" % len(scanned_links))
            fp.write("Total external links found: %s" % len(external_links))
