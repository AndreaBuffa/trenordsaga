import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'main_api'

@endpoints.api(name='discover', version='v1')
class TestApi(remote.Service):
	"""Statistics API v1."""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		trainid=messages.IntegerField(1, variant=messages.Variant.INT32))

	#message_types.VoidMessage
	@endpoints.method(ID_RESOURCE, GreetingCollection,
		path='train_stop_list/{trainid}', http_method='GET',
		name='trains.listStop')
	def greetings_list(self, request):
		return STORED_GREETINGS
