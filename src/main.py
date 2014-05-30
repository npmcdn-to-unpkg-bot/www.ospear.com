# -*- coding: utf-8 -*-

from google.appengine.api import users, mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import datetime
import logging
import traceback

DEFAULT_CHARSET = 'utf-8'
INQUIRY_SUBJECT = u"お問い合わせ通知"
INQUIRY_SENDER = "ooe@ospear.com"
INQUIRY_BCC = "ooe@ospear.com"
INQUIRY_BODY = u'''%s %s様

お問い合わせありがとうございました。
オースピア代表の大江と申します。

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

class JST(datetime.tzinfo):
    def utcoffset(self,dt):
        return datetime.timedelta(hours=0)
    def dst(self,dt):
        return datetime.timedelta(0)
    def tzname(self,dt):
        return "JST"

class MainPage(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        template_values = {
            'user': user,
        }
        self.response.out.write(template.render('web/index.html', template_values))

class ContactPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('web/contact.html', {}))
    
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
            
        template_values = {}
        if len(errors):
            template_values = {
                'office': office,
                'name': name,
                'address': address,
                'tel': tel,
                'email': email,
                'content': content,
                'errors': errors,
                'success': False
            }
        else:
            try:
                office = unicode(office.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                name = unicode(name.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                address = unicode(address.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                tel = unicode(tel.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                email = unicode(email.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                content = unicode(content.encode(DEFAULT_CHARSET), DEFAULT_CHARSET)
                d = datetime.datetime.now(JST()) + datetime.timedelta(hours=9)
                date = d.strftime("%Y-%m-%d %H:%M:%S")
                body = INQUIRY_BODY % (office, name, date, office, name, address, tel, email, content)
                message = mail.EmailMessage(sender=INQUIRY_SENDER, subject=INQUIRY_SUBJECT)
                message.to = email
                message.bcc = INQUIRY_BCC
                message.body = body
                message.send()
            except:
                logging.error(traceback.format_exc())
                template_values = {
                    'errors': {'system_error': True}
                }
            else:
                template_values = {
                    'errors': {},
                    'success': True
                }

        self.response.out.write(template.render('web/contact.html', template_values))

application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/ss', MainPage),
        ('/contact', ContactPage),
    ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
