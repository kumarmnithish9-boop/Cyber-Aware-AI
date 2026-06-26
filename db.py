import sqlite3
import bcrypt
import re
from datetime import datetime, timedelta
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        answer1 TEXT,
        answer2 TEXT,
        answer3 TEXT,
        failed_attempts INTEGER DEFAULT 0,
        lock_until TEXT           
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_scores(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT,
         score INTEGER,
         total_questions INTEGER
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, password, answer1, answer2, answer3):
    answer1 = answer1.strip().lower()
    answer2 = answer2.strip().lower()
    answer3 = answer3.strip().lower()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()

    hashed_answer1 = bcrypt.hashpw(
        answer1.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()

    hashed_answer2 = bcrypt.hashpw(
        answer2.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()

    hashed_answer3 = bcrypt.hashpw(
        answer3.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()


    cursor.execute(
        """
        INSERT INTO users
        (username, password, answer1, answer2, answer3)
        VALUES (?, ?, ?, ?, ?)
        """,
        (username, hashed_password, hashed_answer1, hashed_answer2, hashed_answer3)
    )

    conn.commit()
    conn.close()


def login_user(username, password):

    if username.strip() == "" or password.strip() == "":
        return False

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password = result[0]

        return bcrypt.checkpw(
            password.encode('utf-8'),
            stored_password.encode('utf-8')
        )

    return False

def verify_security_answers(username, a1, a2, a3):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT answer1, answer2, answer3
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if not result:
        return False

    return (
    bcrypt.checkpw(
        a1.strip().lower().encode('utf-8'),
        result[0].encode('utf-8')
    )
    and
    bcrypt.checkpw(
        a2.strip().lower().encode('utf-8'),
        result[1].encode('utf-8')
    )
    and
    bcrypt.checkpw(
        a3.strip().lower().encode('utf-8'),
        result[2].encode('utf-8')
    )
)
def reset_password(username, new_password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (hashed_password, username)
    )

    conn.commit()
    conn.close()

def save_score(username, score, total_questions):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_scores
        (username, score, total_questions)
        VALUES (?, ?, ?)
        """,
        (username, score, total_questions)
    )

    conn.commit()
    conn.close()

def get_scores(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT score, total_questions
        FROM quiz_scores
        WHERE username=?
        """,
        (username,)
    )

    scores = cursor.fetchall()

    conn.close()

    return scores        
    


def delete_user(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )

    conn.commit()
    conn.close()
 

def is_strong_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


def is_account_locked(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT lock_until
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result and result[0]:

        lock_until = datetime.fromisoformat(
            result[0]
        )

        if datetime.now() < lock_until:
            return True

    return False    



def record_failed_login(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT failed_attempts
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    if result:

        attempts = result[0] + 1

        if attempts >= 5:

            lock_until = (
                datetime.now()
                + timedelta(hours=1)
            ).isoformat()

            cursor.execute(
                """
                UPDATE users
                SET failed_attempts = ?,
                    lock_until = ?
                WHERE username = ?
                """,
                (attempts, lock_until, username)
            )

        else:

            cursor.execute(
                """
                UPDATE users
                SET failed_attempts = ?
                WHERE username = ?
                """,
                (attempts, username)
            )

    conn.commit()
    conn.close()

def reset_failed_attempts(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET failed_attempts = 0,
            lock_until = NULL
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()
    conn.close()    



def create_admin():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (username,password,security_question,security_answer)
    VALUES (?,?,?,?)
    """,
    (
        "admin",
        "admin123",
        "Admin",
        "Admin"
    ))

    conn.commit()

    conn.close()    

def get_total_users():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_all_users():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users
        ORDER BY username
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users
def get_total_attempts():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM quiz_scores
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total
def get_best_score():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(score)
        FROM quiz_scores
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return result
def get_all_scores():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username,
               score,
               total_questions
        FROM quiz_scores
        ORDER BY score DESC
        """
    )

    scores = cursor.fetchall()

    conn.close()

    return scores



if __name__ == "__main__":
    create_database()
    create_admin()
    print("Database created successfully")       
