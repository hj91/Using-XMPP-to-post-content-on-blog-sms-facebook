# Author       - Harshad Joshi
# Date         - 10 March 2011
#
# Requirements - XMPP chat server (gtalk)
#              - Python 2.5 with xmpp library.
#
# Features     - Unicode enabled
#
# ToDo         - Add a GUI maybe, and write more good code
# Contains some code from  - Patrick Archibald..http://b.patrickarchibald.com/2010/06/17/email-notification-of-twitter-mentions/

#This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301, USA.


import xmpp
import smtplib
import mimetypes

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64


user='user@gmail.com'
passwd='password'
server='gmail.com'




class Bot:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		connect_object.send(xmpp.Message(message_node.getFrom(),("I am away from my pc right now.  ")))
                gmailUser = user
		gmailPassword = passwd
		recipient = 'you@email.com'
		msg = MIMEMultipart()
		msg['From'] = gmailUser
		msg['To'] = recipient
		msg['Subject'] = command2+" has sent a chat message to you"
		msg.attach(MIMEText(command1))
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmailUser, gmailPassword)
		mailServer.sendmail(gmailUser, recipient, msg.as_string())
		mailServer.close()  				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.sendInitPresence()
        press = xmpp.Presence()
        press.setStatus("Hi from harry the gtalk auto reply bot...Master Harshad has logged in but is away..Type in your IM and i will send it as mail/sms to him :) ")
        connection.send(press)
        
	while (1):
		connection.Process(1)

a=Bot()
a
