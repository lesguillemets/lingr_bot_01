#!/usr/bin/env python2
# coding:utf-8

from __future__ import print_function
from unicodedata import east_asian_width
import string

def _textwidth(text):
    widths = map(east_asian_width,text)
    return len(widths) + widths.count('W')


def sudden_death(text):
    texts = text.split('\n')
    widths = map(_textwidth,texts)
    wholewidth = max(widths)
    suddendeathbody = [
        u"＞　" + u'　'*((wholewidth-width)//4) + txt +
                    u'　'*((wholewidth-width+2)//4) + u"　＜"
        for (width,txt) in zip(widths,texts)
    ]
    header =  u"＿" + u"人"*(wholewidth//2+2) + u"＿"
    footer =  u"￣" + u"Y^"*(wholewidth//2-1) + u"Y" + u"￣"
    return u"\n".join([header]+suddendeathbody+[footer])


if __name__ == "__main__":
    mytxt = u"""\
    あいうえおand there has been
    Hello, World!
    
    """
    print(sudden_death(mytxt).encode("utf-8"))
