import pickle

from django.db import models


class ArrayField(models.CharField):

    """
    Custom django field - child class of CharField - that can write/retrieve Numpy arrays.
    
    """

    def __init__(self, *args, **kwargs):
        models.CharField.__init__(self, *args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        """ Convert the stored database value - a string - into a numpy array. """
        try:
            array = pickle.loads(value)
            return array
        except pickle.PickleError:
            return None

    def get_db_prep_value(self, value, connection, prepared=False):
        """ Convert the input value - a numpy array - into a string for db storing. """
        serialized_array = pickle.dumps(value, protocol=0)
        return serialized_array