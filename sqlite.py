import sqlite3

conn = sqlite3.connect('data/messages.db')
cur = conn.cursor()


def on_start():
    cur.execute('''CREATE TABLE IF NOT EXISTS messages
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       message TEXT);''')


# Добавление сообщения
def add_message(username, user_mes):
    cur.execute("SELECT message FROM messages WHERE username = ?", (username,))
    mes_count = len(cur.fetchall())
    if mes_count < 9:
        cur.execute("INSERT INTO messages (username, message) VALUES(?, ?);", (username, user_mes))
        conn.commit()
        return True
    elif mes_count == 9:
        cur.execute("INSERT INTO messages (username, message) VALUES(?, ?);", (username, user_mes))
        conn.commit()
        return False
    else:
        return False


# Добавление сообщения для премиум пользователя
def add_message_prem(username, user_mes):
    cur.execute("INSERT INTO messages (username, message) VALUES(?, ?);", (username, user_mes))
    conn.commit()


def print_messages():
    cur.execute("SELECT * FROM messages;")
    all_results = cur.fetchall()
    return all_results


async def delete_message_from_db(message_id):
    cur.execute("DELETE FROM messages WHERE id=?;", (message_id,))
    conn.commit()