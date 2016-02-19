import endpoints
from api.surveys import *
package = 'main_api'

handle = endpoints.api_server([SurveysApi])
