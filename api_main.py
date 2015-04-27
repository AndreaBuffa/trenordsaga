import endpoints
from api.statistics import *
from api.schedule import *
from api.discover import *
package = 'main_api'

handle = endpoints.api_server([StatisticsApi, ScheduleApi, DicoverApi])
