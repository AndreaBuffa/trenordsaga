import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'main_api'

class Greeting(messages.Message):
	"""Greeting that stores a message."""
	message = messages.StringField(1)


class GreetingCollection(messages.Message):
	"""Collection of Greetings."""
	items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
	Greeting(message='hello world!'),
	Greeting(message='goodbye world!'),
])


@endpoints.api(name='statistics', version='v1')
class StatisticsApi(remote.Service):
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

	NAME_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		name=messages.StringField(1, variant=messages.Variant.STRING))

	@endpoints.method(NAME_RESOURCE, Greeting,
					path='train_stop_get/{name}', http_method='GET',
					name='trains.getStop')

	def greeting_get(self, request):
		try:
			return STORED_GREETINGS.items[request.name]
		except (IndexError, TypeError):
			raise endpoints.NotFoundException('Greeting %s not found.' %
				(request.name,))
