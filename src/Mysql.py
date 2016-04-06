import mysql.connector

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='reviews')
cursor = cnx.cursor()


class insert:
    def __init__(self, files, messages, sub):
        self.insert(files, messages, sub)

    def insert(self, files, messages, sub):
        add = ("INSERT INTO android"
                        "(files, messages, sub)"
                        "VALUES (%s, %s, %s)")

        data = (files, messages, sub)

        cursor.execute(add, data)
        cnx.commit()
        cursor.close()
        cnx.close()