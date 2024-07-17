#!/usr/bin/env python

__version__ = '0.0.1'

'''
Returns a csv of title, isbn 10, isbn 13, and lexile value from a list of amazon urls.
example:
title, lexile, isbn 10, isbn 13
1984,1090L,9780451524935,978-0451524935
'''

from bs4 import BeautifulSoup
import html5lib, requests
from sys import argv

import argparse
import os

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_title(soup):
    title_span = soup.find('span', attrs = {'id':'productTitle'})
    if title_span:
        return title_span.text.strip()
    return None

def get_isbn10(soup):
    isbn10_outer_div = soup.find('div', attrs = {'id':'rpi-attribute-book_details-isbn10'})
    if isbn10_outer_div:
        isbn10_value_div = isbn10_outer_div.find('div', attrs = {'class':'a-section a-spacing-none a-text-center rpi-attribute-value'})
        return isbn10_value_div.span.text.strip()
    return None

def get_isbn13(soup):
    isbn13_outer_div = soup.find('div', attrs = {'id':'rpi-attribute-book_details-isbn13'})
    if isbn13_outer_div:
        isbn13_value_div = isbn13_outer_div.find('div', attrs = {'class':'a-section a-spacing-none a-text-center rpi-attribute-value'})
        return isbn13_value_div.span.text.strip()
    return None

def get_lexile(soup):
    lexile_outer_div = soup.find('div', attrs = {'id':'rpi-attribute-book_details-lexile'})
    if lexile_outer_div:
        lexile_value_div = lexile_outer_div.find('div', attrs = {'class':'a-section a-spacing-none a-text-center rpi-attribute-value'})
        return lexile_value_div.span.text.strip()
    return None


def get_list_from_file(file):
    links = []
    with open(file, 'r') as contents:
        links = contents.readlines()
    return links



def main():
    links = get_list_from_file(argv[1])

    for link in links:
        request = requests.get(link, headers=HEADERS)

        soup = BeautifulSoup(request.content, 'html5lib')

        # Make sure we're getting a physical book
        # if kindle or audio book then find hardcover


        # if hardcover is going to fail then softcover

        # Product Title
        title_value = get_title(soup)

        # LEXILE
        lexile_value = get_lexile(soup)

        # ISBN_10
        isbn10_value = get_isbn10(soup)

        # ISBN_13
        isbn13_value = get_isbn13(soup)

        print(f"{title_value};{lexile_value};{isbn10_value};{isbn13_value};{link.strip()}", flush = True)

if __name__ == '__main__':
    if len(argv) < 2:
        print('Must provide a file containing a list.')
        exit(1)
    if not os.path.exists(argv[1]):
        print('File does not exist, check path and filename and try again.')
        exit(1)
    main()