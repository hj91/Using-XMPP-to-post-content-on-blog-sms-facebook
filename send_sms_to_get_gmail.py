## check-and-get-gmail-on-phone.py -- A command line util to check GMail and get it on mobile -*- Python -*-
## Harshad Joshi (c) 2011.
## This program is provided 'as-is-what-was' condition...use this code in your program only if you are planning to release it as opensource..

import sys
import urllib             # For BasicHTTPAuthentication
import feedparser         # For parsing the feed
from textwrap import wrap
import gammu
import codecs

_URL = "https://mail.google.com/gmail/feed/atom"

sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()

status = sm.GetSMSStatus()

sms = sm.GetNextSMS(Start = True, Folder = 0)

for ri in sms:
	g=ri['Text']
	f=ri['Number']
	print g

print "\n"+g
h = g.split()

#break the sms into chunks and check for username, passwd and number of mails to receive..ideally this fragment should have some exception handling.  - HJ
if (h[0].lower() == 'check' or h[0] == 'Check'):
		

		uname = str(h[1])
		password = str(h[2])
		maxlen = int(h[3])

		urllib.FancyURLopener.prompt_user_passwd = lambda self, host, realm: (uname, password)
    
def auth():
#'''The method to do HTTPBasicAuthentication'''
    	opener = urllib.FancyURLopener()
    	d = opener.open(_URL)
    	feed = d.read()
    	return feed


def readmail(feed, maxlen):
#'''Parse the Atom feed and print a summary'''
    	atom = feedparser.parse(feed)
    	print '%s new email(s)\n' % (len(atom.entries))
    	for i in range(min(len(atom.entries), maxlen)):
		try:
			message = {'Text':atom.entries[i].author+'>>'+atom.entries[i].title, 'SMSC': {'Location': 1}, 'Number': f }	
			print message['Text']
			sm.SendSMS(message)
                        
		except Exception, e:
			print "boo...!"

    			
if __name__ == "__main__":
	t = auth()  # Do auth and then get the feed
	readmail(t, int(maxlen)) # use feedparser to do some magic. 
		#exit(0)
        
