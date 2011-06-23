# This programs runs on Posterous and logs all the messages sent to it. It can also get comments put by users..  
# Its a sort of federated microblogging with a database backend. Useful for storming sessions.
# Author       - Harshad Joshi
# Date         - 22 June 2011
#
# Requirements - Posterous Blog account
#	       - XMPP chat server (openfire)
#              - Python 2.5 with xmpp and posterous library.
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

import time
import datetime
import posterous
import xmpp
import codecs


user='username@gmail.com'
passwd='gmailpasswd'
server='gmail.com'


#title is not needed for P2 theme. for the rest of themes, date title dosent change. ToDo it.


api = posterous.API('username','passwd')
sites = api.get_sites()


class MyPosterous:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
		c3=command2.replace("@"," [at] ")
		c4=c3.replace("."," [dot] ")		
		#datetitle = datetime.datetime.now()		
		#title = "From xmpp client >> "+command2
		title1 = "What I typed today from IM client >>> "+c4+" " #+str(datetitle)
		if (command1.lower() == 'comment'):
			for post in api.read_posts(id=sites[0].id):
				if post.commentscount > 0:
            				for comment in post.comments:
                				connect_object.send(xmpp.Message(message_node.getFrom(), (comment.body, comment.author)))
				
		else:
			api.new_post(title=title1, body=command1)		
			connect_object.send(xmpp.Message(message_node.getFrom(),("Posted: "+command1)))				
		
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.sendInitPresence()
        presence = xmpp.Presence()
        presence.setStatus("Hi...just send me a message and I will post it on your posterous site")
        connection.send(presence)

	while (1):
		connection.Process(1)

a=MyPosterous()
a

	



