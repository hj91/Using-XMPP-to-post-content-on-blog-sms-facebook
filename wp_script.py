# wp_script.py
# (c) Harshad Joshi, 2011
# Simple script to post new status update on wordpress

from wp_post_class import WP

w=WP('http://localhost/wordpress/xmlrpc.php','admin','harshad',0)
p=raw_input (" Enter a blog post >> ")
w.post(p, "Hi from commandline")
