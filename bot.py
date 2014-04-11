#!/usr/bin/env python
# encoding:utf-8

import webapp2
import json
import re

URLPATTERN = re.compile(r'https?://\S+')

class LingrBot1(webapp2.RequestHandler):
    def __init__(self, *args):
        super(LingrBot1, self).__init__(*args)
        self.commands = {
            '!ping' : self.do_ping,
            '!weather' : self.do_weather,
            '!bf' : self.do_bf,
            '!pyref' : self.do_pyref,
            '!pyref2' : self.do_pyref2,
            '!pyref3' : self.do_pyref3,
            '!random' : self.do_random,
            '!google' : self.do_google,
            '!gimg' : self.do_gimg,
            '!nicodic' : self.do_nicodic,
            '!nicovideo' : self.do_nicovideo,
            '!help' : self.do_help,
            u'今何時ぢゃ' : self.do_koku,
            #'!timezzz' : self.do_timezzz,
        }
    
    def get(self):
        self.response.write("""Hi""")
    
    def post(self):
        #self.do(self.request.body)
        self.do(json.loads(self.request.body))
    
    def do_ping(self, body):
        """Check if bot is online."""
        self.response.write(self.ping())
    
    def do_weather(self, body):
        """Weather forecasts for today and tomorrow.
        usage : !weather <cityname>
        where cityname is one of listed on https://gist.github.com/lesguillemets/f52c57cb19bf25833f3a.
        """
        from modules import weather 
        try:
            forecast = weather.WForecast(body.split()[0]).forecast()
        except ValueError:
            forecast = "Unknown city name. See https://gist.github.com/lesguillemets/f52c57cb19bf25833f3a for a list of the cities for which forecasts are available."
        self.response.write(forecast)
    
    def do_bf(self, body):
        """Brainsth interpreter.
        usage : !bf <command>
        """
        self.response.write("BF intepret result:\n")
        from modules import bf
        mybf = bf.BrainSth(30)
        mybf.give_code(body)
        self.response.write(mybf.execute())
    
    def do_pyref(self, body):
        """Lookup python library reference.
        Usage : !pyref <module name>"""
        from modules import pyref
        self.response.write(pyref.pyref(body))
    
    def do_pyref3(self, body):
        """Lookup python3 library reference.
        Usage : !pyref <module name>"""
        from modules import pyref
        self.response.write(pyref.pyref3(body))
    
    def do_pyref2(self, body):
        """Lookup python2 library reference.
        Usage : !pfref <module name>"""
        from modules import pyref
        self.response.write(pyref.pyref(body, '2'))
    
    def do_random(self, body):
        """Returns random number.
        Usage : !random [int]
        returns random integer 0 <= i < n if n is given,
        otherwise (uniformly) random float in [0.0, 1.0).  """
        import random
        if body:
            try:
                self.response.write(random.randint(0, int(body)))
            except ValueError:
                pass
        else:
            self.response.write(random.random())
    
    def do_nicodic(self, body):
        """Lookup dic.nicovideo.jp.
        Usage : !nicodic <article name>"""
        from modules import nicodic
        self.response.write(nicodic.nicodic(body.encode('utf-8')))
    
    def do_nicovideo(self,body):
        '''search for title and returns the top video.'''
        from modules import nicovideo
        self.response.write("nicovideo response: "+
                            nicovideo.nico_topvideo(body))
    
    '''
    def do_timezzz(self, body):
        """returns datetime.datetime.now()."""
        import datetime as dt
        self.response.write(dt.datetime.now().__repr__())
    '''
    
    def do_google(self, body):
        """Google search."""
        from modules import googlesearch as gs
        self.response.write(gs.gslink(body))
    
    def do_gimg(self, body):
        """Google Image search."""
        from modules import googlesearch as gs
        self.response.write(gs.gslink_img(body))
    
    def do_koku(self, body):
        """Returns current time represented in traditional Japanese style."""
        from modules import etotime
        import datetime as dt
        etime = etotime.ETOTime()
        self.response.write(
            etime.koku(dt.datetime.now() + dt.timedelta(hours=9)) 
            + u" にて候")
    
    def do_help(self, body):
        """Help.
        Usage : !help <command name>
        * bot actions that are not triggered by commands are not supported.
        * command name may or may not include prefixing '!'."""
        if body:
            if body in self.commands:
                self.response.write(self.commands[body].__doc__)
            elif '!' + body in self.commands:
                self.response.write(self.commands['!'+body].__doc__)
            else:
                self.response.write(
                    "Command '{}' not found.".format(body))
        else:
            commandnames = list(map(lambda x: x[1:] if x.startswith('!') else x,
                               self.commands.keys()))
            self.response.write(
            "list of available commands are:\n" +
                ', '.join(commandnames))
    
    def do(self, data):
        message = data['events'][0]['message']
        text = message['text'].strip()
        command = text.split()[0]
        if ' ' in text:
            body = text[text.index(' ')+1:]
        else:
            body = ''
        
        # command execution
        if command in self.commands:
            self.commands[command](body)
        
        elif command[0] == '!' and command[-2:] == 'wp': # wp article
            from modules import wparticle
            langcode = command[1:-2]
            self.response.write(wparticle.wparticle(langcode, body))
        
        else: # not command
            if has_url(text):
                from modules import urltitle
                contained_urls = URLPATTERN.findall(text)
                titles = []
                for urlname in contained_urls:
                    if not urlname.split('.')[-1].lower() in (
                        'png','jpg', 'jpeg', 'gif', 'svg'):
                        titles.append(urltitle.gettitle(urlname))
                if any(titles):
                    self.response.write('URL title response:\n' + '\n'.join(titles))
                else:
                    self.response.write('')
            
            if applicable_suddendeath(text):  # works even when has url
                from modules import suddendeath
                self.response.write(suddendeath.sudden_death(text[1:-1]))
            
            else:  # none of the above
                self.response.write('')
    
    def ping(self):
        return u"I'm online"

def has_url(text):
    return URLPATTERN.search(text) is not None

def applicable_suddendeath(text):
    return ((text.startswith(">") and text.endswith("<")) or
            text.startswith(u"＞") and text.startswith(u"＜"))

application = webapp2.WSGIApplication([('/bot', LingrBot1)], debug=True)
