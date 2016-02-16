from protorpc import messages
from protorpc import message_types

class ColumnProperty(messages.Message):

	type = messages.StringField(1, default='string', required=True)
	id = messages.StringField(2, required=False)
	pattern = messages.StringField(3, required=False)
	p = messages.StringField(4, required=False)

class RowProperty(messages.Message):
	class ValueType(messages.Message):
		pass

	class StringType(ValueType):
		v = messages.StringField(1, required=False)

	c = messages.MessageField(ValueType, 1, required=False)

class DataTable(messages.Message):
	cols = messages.MessageField(ColumnProperty, 1, repeated=True)
	rows = messages.MessageField(RowProperty, 2, repeated=True)

