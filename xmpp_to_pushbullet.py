# This programs runs on a localhost xmpp server and logs all the messages sent to it on Pushbullet.
# Its a sort of federated microblogging with on mobile. Useful for storming sessions.
# Author       - Harshad Joshi
# Date         - 25 April 2014
# Please check the commit data for more details.
#
# Requirements - PushBullet account
#	       - XMPP chat server (openfire)
#              - Python 2.5 with xmpp and PushBullet library.
#
# Features     - Unicode enabled
#
# ToDo         - Bot gets kicked off after being idle for 5 or 6 minutes. 
#              - Needs to send 'KeepALive' packet.
#              - After getting logged in, it posts 'None' as the first message. Need to remove it.
#	       - Dosent work with gtalk. i dont know the reason.
# 	       - Add some more scalability to the bot, ie instead of hardcoding the blog/user/passwd within the program, 
#              - should ask for it once and store it in the backend.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301, USA.





import sys
import pynotify
import time
import datetime
import xmpp
import codecs

user='you@gmail.com'
passwd='your password'
server='gmail.com'

from pushbullet import PushBullet

apiKey = " enter your pushbullet api key from here"
p = PushBullet(apiKey)
# Get a list of devices
devices = p.getDevices()

e=datetime.datetime.now()

PROXY={}
#PROXY={'host':'192.168.0.1','port':3128,'username':'luchs','password':'secret'}



class PushXMPP:
	#this snippet handles presence and subscription...automatically subscribes to user who request subscription. Not recommended for public use.
	def presence_handler(connection_object, message_node):
		prstype=message_node.getType()
		who=message_node.getFrom()
		if prstype == "subscribe":
			connection_object.send (xmpp.Presence(to=who,typ = 'subscribed'))
			connection_object.send (xmpp.Presence(to=who,typ = 'subscribe'))

	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		c3=command2.replace("@"," [at] ")
		c4=c3.replace("."," [dot] ")
		if not pynotify.init("Test Notification"):
			sys.exit(1)
		n = pynotify.Notification("Got this message", command1+ ">>" + command2)
		if not n.show():
			print "Failed to send notification"
		try:
			p.pushNote(devices[0]["id"], command1, command2)
		except Exception, e:
				print 'Error'
				print e
	
		connect_object.send(xmpp.Message(message_node.getFrom(),("Posted: "+command1)))				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	#connection.connect(proxy=PROXY)
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.RegisterHandler('presence',presence_handler,"")
	connection.sendInitPresence()
        presence = xmpp.Presence()
        presence.setStatus("Hi...just send me a message and I will post it masters PushBullet")
        connection.send(presence)

	while (1):
		connection.Process(1)

a=PushXMPP()
a

	



