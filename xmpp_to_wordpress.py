# This programs runs on a localhost xmpp server and logs all the messages sent to it on wordpress blog.
# Its a sort of federated microblogging with a database backend. Useful for storming sessions.
# Author       - Harshad Joshi
# Date         - 10 June 2010
#
# Requirements - Wordpress blog with xml-rpc publishing enabled.
#	       - XMPP chat server (openfire)
#              - Python 2.5 with xmpp and xml-rpc library.
#
# Features     - Unicode enabled
#
# ToDo         - Bot gets kicked off after being idle for 5 or 6 minutes. 
#              - Needs to send 'KeepALive' packet.
#              - After getting logged in, it posts 'None' as the first message. Need to remove it.
#	       - Dosent work with gtalk. i dont know the reason.
# 	       - Add some more scalability to the bot, ie instead of hardcoding the blog/user/passwd within the program, 
#              - should ask for it once and store it in the backend.


blog_name = 'yourblognameatwordpress/xmlrpc.php'
user_name = 'username'
user_pass = 'userpassword'
draft = 0


import sys

import time
import datetime
import xml.sax.saxutils
import xmlrpclib
import xmpp
import codecs

user='user@xmppchatprovider'
passwd='xmppuserpasswd'
server='xmppserver'

e=datetime.datetime.now()

#title is not needed for P2 theme. for the rest of themes, date title dosent change. ToDo it.


blog_id = 0

class WP:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		c3=command2.replace("@"," [at] ")
		c4=c3.replace("."," [dot] ")		
		#datetitle = datetime.datetime.now()		
		#title = "From xmpp client >> "+command2
		title = "What I typed today from IM client >>> "+c4+" " #+str(datetitle)
		if (command1 != 'None'):
			blog_content = { 'title' : str(title), 'description' : command1+"\n"+">> "+c4 }
			categories = [{'categoryId' : 'Links', 'isPrimary' : 1}]
			try:
				sp = xmlrpclib.ServerProxy(blog_name)
				post_id = int(sp.metaWeblog.newPost(blog_id, user_name, user_pass, blog_content, not draft))
				sp.mt.setPostCategories(post_id, user_name, user_pass, categories)
				sp.mt.publishPost(post_id, user_name, user_pass)
			except Exception, e:
				print 'XML-RPC not enabled on your WP blog.'
				print e
	
		connect_object.send(xmpp.Message(message_node.getFrom(),("Posted: "+command1)))				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.sendInitPresence()
        presence = xmpp.Presence()
        presence.setStatus("Hi...just send me a message and I will post it on http://moiblogging.wordpress.com")
        connection.send(presence)

	while (1):
		connection.Process(1)

a=WP()
a

	



