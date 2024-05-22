import mysql.connector

conn = mysql.connector.connect (
                                    host = "127.0.0.1",
                                      user = 'root',
                                      password = '',
                                      database = 'task')

cursr = conn.cursor(dictionary=True)
