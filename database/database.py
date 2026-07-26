import sqlite3

DATABASE_NAME = "bostonpharmacy.db"


def get_connection():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        profile_image TEXT DEFAULT '',

        xp INTEGER DEFAULT 0,

        level TEXT DEFAULT 'Beginner Pharmacy Technician',

        ptcb_attempts INTEGER DEFAULT 0,

        ptcb_best_score INTEGER DEFAULT 0,

        ptcb_correct INTEGER DEFAULT 0,

        ptcb_wrong INTEGER DEFAULT 0

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        module_name TEXT,

        completed INTEGER DEFAULT 0,

        xp_earned INTEGER DEFAULT 0,

        FOREIGN KEY(user_id)

        REFERENCES users(id)

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        achievement TEXT,

        date TEXT,

        FOREIGN KEY(user_id)

        REFERENCES users(id)

    )
    """)

    conn.commit()

    conn.close()


def register_user(full_name, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users
        (full_name, email, password)
        VALUES (?, ?, ?)
        """, (full_name, email, password))

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE email=?

    AND password=?

    """,

    (email, password)

    )

    user = cursor.fetchone()

    conn.close()

    return user
def update_profile_image(user_id, image_path):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users

        SET profile_image=?

        WHERE id=?

        """,

        (
            image_path,
            user_id
        )

    )

    conn.commit()
    conn.close()


def add_achievement(user_id, achievement):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO achievements

        (user_id, achievement, date)

        VALUES (?, ?, datetime('now'))

        """,

        (
            user_id,
            achievement
        )
    )


    conn.commit()

    conn.close()



def get_achievements(user_id):

    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT achievement
        FROM achievements
        WHERE user_id=?
        """,
        (user_id,)
    )

    achievements = cursor.fetchall()

    conn.close()

    return achievements


def save_module_progress(user_id, module_name, xp):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO progress
        (user_id, module_name, completed, xp_earned)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            module_name,
            1,
            xp
        )
    )

    cursor.execute(
        """
        UPDATE users
        SET xp = xp + ?
        WHERE id = ?
        """,
        (
            xp,
            user_id
        )
    )

    conn.commit()
    conn.close()


def update_database():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN ptcb_weak_areas TEXT DEFAULT ''
            """
        )

    except:

        pass

    try:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN ptcb_correct INTEGER DEFAULT 0
            """
        )

    except:

        pass

    try:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN ptcb_wrong INTEGER DEFAULT 0
            """
        )

    except:

        pass

    conn.commit()

    conn.close()