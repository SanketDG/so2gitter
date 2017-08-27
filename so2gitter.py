import json
import xmltodict
import requests
import os

SITE_URL = "https://stackoverflow.com/feeds/tag"



def get_feed_response(url, tag):

    response = requests.get(url, params={'tagnames': tag, 'sort': 'newest'})

    # print(response.url, response, response.text)

    if(response.status_code == 200):
        return response.text

def yield_processed_dict(json_response):

        for entry in json_response['feed']['entry']:
            yield "[{0}]({1})".format(entry['title']['#text'], entry['id'])

def send_to_gitter(question):
    response = requests.post(os.getenv("GITTER_WEBHOOK_URL"), data={'message': question})

def main():
    response = get_feed_response(SITE_URL, "coala")

    response_dict = xmltodict.parse(response)

    for question in yield_processed_dict(response_dict):
        send_to_gitter(question)


if __name__ == '__main__':
    main()
