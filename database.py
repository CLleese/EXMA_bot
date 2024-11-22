import psycopg2
from datetime import datetime
from datetime import timedelta
import config

host = config.host
user = config.user
password = config.password
db_name = config.db_name


def addUser(id, register_time, count_of_get_spam, username):
    try:
        connection = psycopg2.connect(host= host, user= user, password= password, database= db_name)
        username = '{'+str(username)+'}'

        with connection.cursor() as cursor:
            cursor.execute(f""" 
                    INSERT INTO users(id, time, count, username) VALUES (
                           {id},
                           {register_time},
                           {count_of_get_spam},
                           %s
                           )
                    """, [username])
            connection.commit()
            print("[INFO] New user is here!")

    except Exception as ex:
        print("Something wrong!: ", ex)

    finally:
        connection.close()
        print("[INFO] connection is closed")


def checkUsers():
    try:
        connection = psycopg2.connect(host= host, user= user, password= password, database= db_name)

        users = []

        with connection.cursor() as cursor:
            cursor.execute(f"""
                           SELECT * FROM users 
                           WHERE date_trunc('day', to_timestamp(time) + interval '1 seconds') = date_trunc('day', now() AT TIME ZONE 'UTC')""");
            result = cursor.fetchall()
            for r in result:
                print("[INFO] This guy is as: ", r[0])
                users.append([r[0], r[2]])
                cursor.execute(f"""UPDATE users SET count = count+1 WHERE id = {r[0]}""")

            connection.commit()
            print("[INFO] Method is done succesfully")
            

    except Exception as ex:
        print("Something wrong!: ", ex)

    finally:
        connection.close()
        for u in users:
            print("[INFO] that users: ", u)
        print("[INFO] connection is closed")
        return users

