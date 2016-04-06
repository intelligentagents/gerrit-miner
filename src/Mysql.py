import mysql.connector

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='reviews')
cursor = cnx.cursor()

class Insert:
    def __init__(self, files, messages, comments, sub):
        self.insert(files, messages, comments, sub)

    def is_empty(self, json):
        if json:
            self.insertIntoMongo(json);
        else:
            print("vazio")

    def insert(self, files, messages, comments, sub):
        add_employee = ("INSERT INTO android"
                        "(files, menssages, comments, sub) "
                        "VALUES (%s, %s, %s, %s)")

        data_employee = (files, messages, comments, sub)

        cursor.execute(add_employee, data_employee)
        cnx.commit()
        cursor.close()
        cnx.close()




