from macpath import split

__author__ = 'semyon'

from connector import Connector


class Tester:
    def __init__(self, connector):
        self.connector = connector

    def test_message(self, message):
        lst = message.split()
        distinct = []
        for a in lst:
            if not a in distinct:
                distinct.append(a)
        connector = self.connector
        s_vals = []
        for word in distinct:
            s_vals.append(connector.get_spam_probability_of_word(word))
        nominator = 1
        for val in s_vals:
            nominator *= val
        denominator = 1
        for val in s_vals:
            denominator *= (1 - val)
        denominator += nominator
        probability = nominator / denominator
        if probability > 0.5:
            print "True"
        else:
            print "False"