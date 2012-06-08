# Generic class for posting new update on wordpress blog.
# ToDo - Add some more features to to read, edit blog posts
# (c) Harshad Joshi, 2011 


import xmlrpclib

class WP:
	def __init__(self,blog_name,user_name,user_pass,blog_id):
		self.blog_name = blog_name #'http://localhost/wordpress/xmlrpc.php'
		self.user_name = user_name #'admin'
		self.user_pass = user_pass #'harshad'
		self.blog_id=0
		self.draft = 0
		self.simulation = 0
	
	def post(self,a,title):
		'''Contains XML-RPC procedures'''
		self.a= a # raw_input (" Enter a blog post >> ")
		self.title = title #"Sent via IM client "#>>> "+c4+" " #+str(datetitle)
		blog_content = { 'title' : str(self.title), 'description' : self.a+"\n" }
		categories = [{'categoryId' : 'Links', 'isPrimary' : 1}]
		sp = xmlrpclib.ServerProxy(self.blog_name)
		post_id = int(sp.metaWeblog.newPost(self.blog_id, self.user_name, self.user_pass, blog_content, not self.draft))
		sp.mt.setPostCategories(post_id, self.user_name, self.user_pass, categories)
		sp.mt.publishPost(post_id, self.user_name, self.user_pass)




