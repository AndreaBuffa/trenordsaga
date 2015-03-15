import webapp2
import mean
from google.appengine.ext import deferred

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(mean.Mean)
        self.response.out.write('Schema migration successfully initiated.')

app = webapp2.WSGIApplication([('/mean', UpdateHandler)])