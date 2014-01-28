#!/usr/bin/python
# encoding:utf-8
import urllib2 as ul
import re
import HTMLParser

def gettitle(url):
    _htmlparser = HTMLParser.HTMLParser()
    titlematch = re.compile(r'<title>(.*?)</title>', 
                            re.DOTALL|re.IGNORECASE|re.U)
    googlesearch = re.compile(
        r"https?://www\.google\.((co\.[a-z]{2,3})|(com))/(#|search\?)\w+")
    googlekeyword = re.compile(r"q=([^&]+)")
    
    if googlesearch.search(url):
        query = googlekeyword.search(url).group(1)
        if 'tbm=isch' in url:
            return ("Google Image search: " + 
                    ul.unquote(query.encode("utf-8")).replace("+",' '))
        else:
            return ("Google search: " + 
                    ul.unquote(query.encode("utf-8")).replace("+",' '))
    
    elif url.startswith("https://gist.github.com"):
        return ""
    
    else:
        try:
            req = ul.Request(url)
            '''
            req.add_header('User-agent',
                           'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0')
            '''
            U = ul.urlopen(req)
            if U.getcode() == 200:
                html = U.read()
            elif U.getcode() == 404:
                return  "Not Found."
            else:
                return "Got code {}".format(U.getcode())
        except ValueError as e:
                return e
        except ul.HTTPError as e:
            return e.reason
        except ul.URLError as e:
            return e.reason
        except:
            return ''
        
        try:
            return _htmlparser.unescape(
                titlematch.search(html).group(1).decode('utf-8'))
        except:
            return ''

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        for url in sys.argv[1:]:
            print(gettitle(url))
    else:
        print(gettitle('https://ja.wikipedia.org/wiki/%E3%81%BF%E3%81%8B%E3%82%93'))
        print(gettitle("http://URL_THAT_DOES_NOT_EXIST"))
        print(gettitle("http://lesguillemets.blogpot.com/ajgioetb"))
        #print(gettitle("ejtihojateo"))
