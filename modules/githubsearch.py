#!/usr/bin/env python2
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
    return response['items'][0]

def lingr_github_search(keyword):
    item = github_best_match(keyword)
    return dedent("""\
        {fullname} ({url})
        \t {descr}
        written in {lang} / {fk} forks / {st} stars
        homapage : {hp}""".format(
            fullname = item['full_name'],
            url = item['html_url'],
            descr = item['description'],
            lang = item['language'],
            fk = item['forks_count'],
            st = item['stargazers_count'],
            hp = item['homepage'],
        ))


if __name__ == "__main__":
    print(lingr_github_search("Twython"))


