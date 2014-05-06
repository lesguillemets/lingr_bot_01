#!/usr/bin/env python2
# coding:utf-8
'''
Interface for github search.
'''
try:
    from modules import const
except ImportError:
    import const
import urllib2 as ul
from textwrap import dedent
import contextlib
import json
import pprint

SEARCH_BASE_URL = dedent('\
    https://api.github.com/search/repositories?client_id={}&client_secret={}{}'\
    .format(const.github_app['client_id'], const.github_app['client_secret'],
            '{}')
    )

def github_best_match(keyword):
    with contextlib.closing(
        ul.urlopen(SEARCH_BASE_URL.format(
            '&q=' + '+'.join(keyword.split())
        ))
    ) as u:
        response = json.loads(u.read())
    try:
        return response['items'][0]
    except IndexError:
        return None

def lingr_github_search(keyword):
    item = github_best_match(keyword)
    if item:
        return dedent("""\
            {fullname} ( {url} )
            \t {descr}
            written in {lang} / {fk} forks / {st} stars
            homapage : {hp}""".format(
                fullname = item['full_name'].encode("utf-8"),
                url = item['html_url'],
                descr = (
                    item['description'].encode("utf-8") if item['description']
                         else 'None'),
                lang = (
                    item['language'].encode("utf-8") if item['language']
                        else "[no data]"),
                fk = item['forks_count'],
                st = item['stargazers_count'],
                hp = (
                    item['homepage'].encode("utf-8") if item['homepage']
                      else "None"),
            ))
    else:
        return "Couldn't find repositories matching '{}'.".format(keyword)

if __name__ == "__main__":
    print(lingr_github_search("twython"))
    print(lingr_github_search("notarepository"))
