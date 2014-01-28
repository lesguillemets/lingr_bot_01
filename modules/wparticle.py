#!/usr/bin/env python2
# coding:utf-8

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import urllib2 as url
from urllib import quote
import xml.etree.ElementTree as elm

def wparticle(langcode, articlename):
    """
    'ja' -> Unicode -> str
    """
    
    if wp_has_article(langcode, articlename):
        wpurl = "https://{}.wikipedia.org/wiki/{}".format(
                    langcode, quote(articlename.encode("utf-8")))
        return wpurl
    
    else:
        wpsearch = "https://{}.wikipedia.org/wiki/Special:search/{}".format(
            langcode, quote(articlename.encode("utf-8")))
        return '"{}" : 項目が見つかりません．検索結果: {}'.format(
            articlename.replace('_',' '), wpsearch).encode("utf-8")
        


def wp_has_article(langcode, articlename):
    """
        articlename is assumed to be type unicode.
    """
    query = "http://{}.wikipedia.org/w/api.php?action=query&titles={}&format=xml".format(
        langcode, quote(articlename.encode("utf-8")))
    q = url.urlopen(query)
    page = q.read()
    q.close()
    root = elm.fromstring(page)
    for page in root.iter('page'):
        return not('missing' in page.attrib)

