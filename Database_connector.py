import mysql.connector


from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    database=MYSQL_DB
)


def mycursor():
    cursor = db.cursor(dictionary=True)

    return cursor


def get_details(query):
    cur = db.cursor()
    cur.execute(query)
    answer = []
    for row in cur.fetchall():
        answer.append(row)
    return answer
