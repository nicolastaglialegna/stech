import mysql.connector
from mysql.connector import Error

consult = False
insert = True


class data(object):
    def __init__(self, vendor, model, softversion):
        self.vendor = vendor
        self.model = model
        self.softversion = softversion


def sql_consult(vendor, model, softversion):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='company',
                                             port='3316',
                                             user='root',
                                             password='stech',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            sql_select_Query = f"""SELECT * FROM cm_models WHERE vendor = '{vendor}' or model = '{model}' or softversion = '{softversion}';"""
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()

            if len(records) < 1:
                in_db = False
            else:
                in_db = True

    except Error as e:
        print("Error while connecting to MySQL", e)
        return True, []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return in_db, records


def mysql_insert(vendor, model, softversion):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='company',
                                             port='3316',
                                             user='root',
                                             password='stech',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            mySql_insert_query = f"""INSERT INTO cm_models (vendor, model, softversion) VALUES ('{vendor}', '{model}', '{softversion}') """
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return [(vendor, model, softversion)]


def mysql_conection(consul: False, insert: False):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='company',
                                             port='3316',
                                             user='root',
                                             password='stech',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            if consult:
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                sql_select_Query = "select * from cm_models;"
                cursor = connection.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()

                for row in records:
                    print("Vendor: {0}, Model: {1}, softversion: {2}".format(
                        row[0], row[1], row[2]))

            if insert:
                vendor = 'prueba2'
                model = 'prueba2'
                softversion = 'prueba2'

                mySql_insert_query = f"""INSERT INTO cm_models (vendor, model, softversion) VALUES ('{vendor}', '{model}', '{softversion}') """
                cursor = connection.cursor()
                cursor.execute(mySql_insert_query)
                connection.commit()
                print(cursor.rowcount,
                      "Record inserted successfully into cm_models table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
