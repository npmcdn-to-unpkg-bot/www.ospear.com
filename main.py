#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import traceback
import datetime
import cgi
import json
from google.appengine.api import mail

class JST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=0)
    def dst(self, dt):
        return datetime.timedelta(0)
    def tzname(self,dt):
        return "JST"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class ContactHandler(webapp2.RequestHandler):
    CHARSET = 'utf-8'
    SUBJECT = u"お問い合わせ通知"
    SENDER = "ooe@ospear.com"
    BCC = "ooe@ospear.com"
    BODY = u'''%s %s様

お問い合わせありがとうございました。
オースピアの大江と申します。

下記内容でお問い合わせを受け付けました。
ご回答まで今しばらくお待ちください。

=======================================
お問い合わせ日時: %s
会社名/店舗名: %s
担当者名: %s
住所: %s
電話番号: %s
メールアドレス: %s
お問い合わせ内容:
%s
=======================================

--
Web開発事務所オースピア代表
大江 好充 <ooe@ospear.com>
'''

    def post(self):
        logging.info(self.request)

        office = cgi.escape(self.request.get('office'))
        name = cgi.escape(self.request.get('name'))
        address = cgi.escape(self.request.get('address'))
        tel = cgi.escape(self.request.get('tel'))
        email = cgi.escape(self.request.get('email'))
        content = cgi.escape(self.request.get('content'))

        errors = {}
        if not len(office):
            errors['office'] = 'blank'
        if not len(name):
            errors['name'] = 'blank'
        if not len(email):
            errors['email'] = 'blank'
        elif not mail.is_email_valid(email):
            errors['email'] = 'invalid'
        if not len(content):
            errors['content'] = 'blank'

        if len(errors):
            self._writeJson({errors: errors})
            return
        try:
            office = unicode(office.encode(self.CHARSET), self.CHARSET)
            name = unicode(name.encode(self.CHARSET), self.CHARSET)
            address = unicode(address.encode(self.CHARSET), self.CHARSET)
            tel = unicode(tel.encode(self.CHARSET), self.CHARSET)
            email = unicode(email.encode(self.CHARSET), self.CHARSET)
            content = unicode(content.encode(self.CHARSET), self.CHARSET)
            now = datetime.datetime.now(JST()) + datetime.timedelta(hours=9)
            strNow = now.strftime("%Y-%m-%d %H:%M:%S")
            body = self.BODY % (
                office, name, strNow, office, name, address, tel, email, content
            )
            self._sendMail(email, body)
        except:
            logging.error(traceback.format_exc())
            self._writeJson({'errors': {'system_error': True}})
        else:
            self._writeJson({'success': True})

    def _writeJson(self, obj):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(obj))

    def _sendMail(self, to, body):
        #mail.send_mail(SENDER, to, SUBJECT, body)
        message = mail.EmailMessage(sender=self.SENDER, subject=self.SUBJECT)
        message.to = to
        message.bcc = self.BCC
        message.body = body
        message.send()

app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/contact', ContactHandler)
], debug=True)

