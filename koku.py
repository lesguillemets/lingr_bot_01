#!/usr/bin/env python
# coding: utf-8

import webapp2
from modules import etotime

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
        self.response.write(HTML_TEMP.format(etime.koku() + u" にて候"))
    
application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
