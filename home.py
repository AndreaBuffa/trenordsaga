import webapp2
from controller import Controller

app = webapp2.WSGIApplication([
	('/', Controller)
])

print "home"
