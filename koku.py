#!/usr/bin/env python
# coding: utf-8

import webapp2
from modules import etotime
import datetime as dt

HTML_TEMP = u"""\
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>今何時ぢゃ</title>
</head>
<body>
  {}
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        etime = etotime.ETOTime()
        self.response.write(
            HTML_TEMP.format(
                etime.koku(dt.datetime.now() + dt.timedelta(hours=9))
                + u" にて候")
        )
    
application = webapp2.WSGIApplication([('/koku', MainHandler)], debug=True)
