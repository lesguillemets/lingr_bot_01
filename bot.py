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
            '!timezzz' : self.do_timezzz,
            u'今何時ぢゃ' : self.do_koku,
        }
    
    def get(self):
        self.response.write("""Hi""")
    
    def post(self):
        #self.do(self.request.body)
        self.do(json.loads(self.request.body))
    
    def do_ping(self, body):
        self.response.write(self.ping())
    
    def do_weather(self, body):
        from modules import weather 
        forecast = weather.WForecast(text.split()[1]).forecast()
        self.response.write(forecast)
    
    def do_bf(self, body):
        self.response.write("BF intepret result:\n")
        from modules import bf
        mybf = bf.BrainSth(30)
        mybf.give_code(body)
        self.response.write(mybf.execute())
    
    def do_pyref(self, body):
        from modules import pyref
        self.response.write(pyref.pyref(body))
    
    def do_pyref3(self, body):
        from modules import pyref
        self.response.write(pyref.pyref3(body))
    
    def do_pyref2(self, body):
        from modules import pyref
        self.response.write(pyref.pyref(body, '2'))
    
    def do_random(self, body):
        import random
        if body:
            try:
                self.response.write(random.randint(0, int(body)))
            except ValueError:
                pass
        else:
            self.response.write(random.random())
    
    def do_nicodic(self, body):
        from modules import nicodic
        self.response.write(nicodic.nicodic(body.encode('utf-8')))
    
    def do_timezzz(self, body):
        import datetime as dt
        self.response.write(dt.datetime.now().__repr__())
    
    def do_google(self, body):
        from modules import googlesearch as gs
        self.response.write(gs.gslink(body))
    
    def do_gimg(self, body):
        from modules import googlesearch as gs
        self.response.write(gs.gslink_img(body))
    
    def do_koku(self, body):
        from modules import etotime
        import datetime as dt
        etime = etotime.ETOTime()
        self.response.write(
            etime.koku(dt.datetime.now() + dt.timedelta(hours=9)) 
            + u" にて候")
    
    
    def do(self, data):
        message = data['events'][0]['message']
        text = message['text']
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
                if titles != []:
                    self.response.write('URL title response:\n' + '\n'.join(titles))
                else:
                    self.response.write('')
            
            else:  # none of the above
                self.response.write('')
    
    def ping(self):
        return u"I'm online"

def has_url(text):
    return URLPATTERN.search(text) is not None

application = webapp2.WSGIApplication([('/bot', LingrBot1)], debug=True)
