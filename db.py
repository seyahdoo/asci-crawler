import pymongo

import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["linkedin-bot"]
links = mydb["links"]

max_depth_to_search = 0

def get_one_link():

    link = links.find_one({"is_crawled": False,"depth_from_relative":{"$lte":max_depth_to_search}})

    if not link:
        print ("finished crawling")
        exit(0)

    return link


profile_regex = re.compile("https?://(www.)?linkedin.com/in/.*?")
company_regex = re.compile("https?://(www.)?linkedin.com/company/.*?")
mynetwork_regex = re.compile("https?://(www.)?linkedin.com/mynetwork/.*?")
search_regex = re.compile("https?://(www.)?linkedin.com/search/results/.*?")

def add_link(from_url, new_url, new_depth):

    #from_url = from_url.lower()
    new_url = new_url.lower()

    existing = links.find_one({"url":new_url})

    if existing:
       return

    page_type = "default"
    if profile_regex.match(new_url):
        # add profile as profile
        # https://www.linkedin.com/in/selenayunlutas/
        # add with remaining as default
        # https://www.linkedin.com/in/selenayunlutas/xxxxxxxxxxxxxxxx
        page_type = "profile"
    elif company_regex.match(new_url):
        page_type = "company"
    elif search_regex.match(new_url):
        page_type = "search"
    elif mynetwork_regex.match(new_url):
        page_type = "mynetwork"

    links.insert_one(
        {
            "url": new_url,
            "is_relative": False,
            "depth_from_relative": new_depth,
            "is_crawled": False,
            "page_type": page_type,
        })

    return


def mark_crawled(link):
    existing = links.find_one({"url": link})

    if not existing:
        print("Problem at -> "+ link)

    links.find_one_and_update({"url":link},{"$set":{"is_crawled":True}})
    return


def mark_relative(link):
    existing = links.find_one({"url": link})

    if not existing:
        print("Problem at -> " + link)

    links.find_one_and_update({"url": link}, {"$set": {"is_relative": True}})

    mark_depth(link,0)

    return


def mark_depth(link, new_depth):
    existing = links.find_one({"url": link})

    if not existing:
        print("Problem at -> " + link)

    links.find_one_and_update({"url": link}, {"$set": {"depth_from_relative": new_depth}})
    return

def get_depth(link):
    existing = links.find_one({"url": link})

    if not existing:
        print("Problem at -> " + link)

    return existing["depth_from_relative"]


if __name__ == "__main__":

    #add_link(None, "https://www.linkedin.com/in/oguzalptan/", 0)
    add_link(None, "https://www.linkedin.com/in/selenayunlutas/", 0)
    #add_link(None, "https://www.linkedin.com/mynetwork/",0)
    #add_link(None, "https://www.linkedin.com/in/oguzalptan/", 0)
    #add_link(None, "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22164857%22%5D", 0)
    #add_link(None, "https://www.linkedin.com/in/leman-bezci-0452a7b7/", 0)
    #add_link(None, "https://www.linkedin.com/in/seyahdoo/", 0)
