#!/usr/bin/env python2
# coding:utf-8

import urllib2 as ul
import datetime as dt
import re
#from xml.dom import minidom

def jstnow():
    return dt.datetime.now() + dt.timedelta(hours=9)

class XMLData(object):
    
    def __init__(self, xmlstring):
        self.xml = xmlstring  # str!
    
    def gettag(self,tagname):
        pattern = re.compile(r'<{}>(.*)</{}>'.format(tagname,tagname))
        return pattern.search(self.xml).group(1)

def strtoddm(string):
    hour, minute = map(int,string.split(':'))
    return dt.time(hour=hour, minute=minute)


class ETOTime(object):
    
    eto = [u'子', u'丑', u'寅', u'卯', u'辰', u'巳',
           u'午', u'未', u'申', u'酉', u'戌', u'亥']
    kanjinum = [u'一', u'二', u'三', u'四']
    
    def __init__(self, cityname = u"京都府京都市"):
        self.cityname = cityname
        self.set_sun_time()
        self.set_koku_length()
    
    def koku(self, time = jstnow()):
        chour = time.hour + time.minute / 60.0
        if self.sunrise < chour < self.sunset:  # if daytime:
            n = int((chour - self.sunrise) // self.day_koku)
            koku, tsu = divmod(n+2, 4)
            return self.eto[koku+3] + self.kanjinum[tsu] + u"つ"
        else:
            if chour < self.sunrise: # morning
                n = int(chour // self.night_koku)
                koku, tsu = divmod(n+2, 4)
                return self.eto[koku] + self.kanjinum[tsu] + u"つ"
            
            else:  # night
                n = int((chour - self.sunset) // self.night_koku)
                koku, tsu = divmod(n+2, 4)
                return self.eto[(koku+9)%12] + self.kanjinum[tsu] + u"つ"
                # %12 required for 子.

    
    def set_sun_time(self, date_=jstnow()):
        
        if isinstance(self.cityname, str):
            city_encoded = ul.quote(self.cityname)
        elif isinstance(self.cityname, unicode):
            city_encoded = ul.quote(self.cityname.encode('utf-8'))
        mode = 'sun_rise_set'
        timequery = "year={}&month={}&day={}".format(
                                date_.year, date_.month, date_.day)
        req = ul.urlopen(
          'http://labs.bitmeister.jp/ohakon/api/?mode={}&{}&address={}'.format(
                mode, timequery, city_encoded)
        )
        data = req.read()
        req.close()
        xmldata = XMLData(data)
        self.sunrise = float(xmldata.gettag('sunrise'))
        self.sunset = float(xmldata.gettag('sunset'))
        self.sunrise_hm = strtoddm(xmldata.gettag('sunrise_hm'))
        self.sunset_hm = strtoddm(xmldata.gettag('sunset_hm'))
        self.today = date_
        #print data
    
    def set_koku_length(self):
        try:
            self.day_koku = (self.sunset - self.sunrise) / 24
            self.night_koku = (24 - (self.sunset - self.sunrise)) / 24
        except AttributeError:
            self.set_sun_time()
            self.set_koku_length()



if __name__ == "__main__":
    y= ETOTime()
    print y.koku(dt.datetime(2013,1,15,13,0)).encode('utf-8')
