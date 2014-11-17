from __future__ import division

__author__ = 'semyon'
import MySQLdb



def in_quotes(word):
    return "'" + word + "'"


class Connector:
    def __init__(self, user, password, host, db, types_to_table_names):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.table_names = types_to_table_names

        # if not "spam" in types_to_table_names: error
        # if not "ham" in types_to_table_names: error

        pass

    def __get_connection(self):
        return MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.password,
                               db=self.db)

    def put_data(self, word, is_spam):
        word_type = "spam" if is_spam else "ham"
        table_name = self.table_names[word_type]
        conn = self.__get_connection()
        exists = self.exists(word, word_type)
        statement = ""
        if exists:
            new_val = int(self.get_value(word, word_type)) + 1
            statement = "UPDATE " + table_name + " set value=" + `new_val` + " WHERE word=" + in_quotes(word) + ";"
        else:
            statement = "INSERT INTO " + table_name + " (word, value)" + " VALUES(" + in_quotes(word) + "," + `1` + ");"
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.commit()

    def exists(self, word, word_type):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + self.table_names[word_type] + " WHERE word = " + in_quotes(word) + ";")
        row = cursor.fetchone()
        return row[0] >= 1

    def get_value(self, word, word_type):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM " + self.table_names[word_type] + " WHERE word = " + in_quotes(word) + ";")
        row = cursor.fetchone()
        return row[0]

    def get_spam_probability_of_word(self, word):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM spam WHERE word = " + in_quotes(word) + ";")
        row = cursor.fetchone()
        spammy = 0
        hammy = 0
        if row:
            spammy = int(row[0])
        cursor.execute("SELECT value FROM ham WHERE word = " + in_quotes(word) + ";")
        row = cursor.fetchone()
        if row:
            hammy = int(row[0])
        if spammy == 0 and hammy == 0:
            return 0.5
        if spammy == 0:
            return 1.0
        probability = spammy / (spammy + hammy)
        return probability

