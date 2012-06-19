#!/usr/bin/python
#CLI to send xmpp message to specified user
#Does not verify if user is present in roster list or not.
#Does not do size checking for txt in argument
#Harshad Joshi

import sys,os,xmpp,time

user='youid@gmail.com'
passwd=''
server='gmail.com'


if len(sys.argv) < 2:
    print "Syntax: xsend JID text"
    sys.exit(0)

tojid=sys.argv[1]
text=' '.join(sys.argv[2:])

jid=xmpp.JID(user)
cl=xmpp.Client(jid.getDomain(),debug=[])

con=cl.connect()
if not con:
    print 'could not connect!'
    sys.exit()
print 'connected with',con
auth=cl.auth(jid.getNode(),passwd)
if not auth:
    print 'could not authenticate!'
    sys.exit()
print 'authenticated using',auth

#cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
id=cl.send(xmpp.protocol.Message(tojid,text))
print 'sent message with id',id

time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending

#cl.disconnect()
