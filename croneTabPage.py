import webapp2

class CroneTabPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, chornetab!')

app = webapp2.WSGIApplication([
    ('/', CroneTabPage),
], debug=True)

