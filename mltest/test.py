__author__ = 'semyon'

from connector import Connector
from tester import Tester

connector = Connector("pythonroot", "test", "localhost", "mlt", {"spam": "spam", "ham": "ham"})
#connector.put_data("asd", True)
tester = Tester(connector)
tester.test_message("Qwerty asd")


