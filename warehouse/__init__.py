"""
This module uses the `__init__` file to initialize the database connection and create the necessary tables. 
Once the tables are created, the database is ready for interaction as soon as it is imported into other modules or external applications.
"""

import sqlite3

tables_statment = [
    """CREATE TABLE IF NOT EXISTS members(
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """,
    """CREATE TABLE IF NOT EXISTS activities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(name IN('bodybuilding', 'crossfit', 'mixed_arts'))
    );
    """,
    """CREATE TABLE IF NOT EXISTS subscriptions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT NOT NULL,
        activity_id INTEGER NOT NULL,
        subscription_method TEXT CHECK(subscription_method IN ('monthly', '20_session', '30_session')),
        subscription_start_date DATE NOT NULL,
        subscription_end_date DATE,  -- Only applicable for monthly subscriptions,
        remaining_sessions INTEGER,  -- Only applicable for session-based subscriptions,
        FOREIGN KEY (member_id) REFERENCES users(user_id),
        FOREIGN KEY (activity_id) REFERENCES activities(id)
    );
    """,
    """CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT NOT NULL,
        visit_date DATE NOT NULL,
        activity_id INTEGER NOT NULL,
        FOREIGN KEY (member_id) REFERENCES users(user_id),
        FOREIGN KEY (activity_id) REFERENCES activities(id)
    );
    """
]

def create_tables():
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()

            # Execute table creation statements
            for statement in tables_statment:
                cursor.execute(statement)
            
            conn.commit()  # Commit changes
            print('Tables created successfully.')
    except sqlite3.OperationalError as e:
        print("Failed to create tables:", e)

# Call the create_tables function to initialize the database
create_tables()

def create_activity(activity):
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()
            #! Check if activity already exists before inserting
            cursor.execute('SELECT id FROM activities WHERE name = ?', (activity,))
            existing_activity = cursor.fetchone()
            if existing_activity:
                print(f"Activity '{activity}' already exists. Skipping insertion.")
            else:
                cursor.execute('''INSERT INTO activities(name) VALUES(?)''', (activity,))
                conn.commit()
                print(f"Successfully inserted activity: {activity}")
    except sqlite3.OperationalError as e:
        print("Failed to insert activity into database. OperationalError:", e)
    except sqlite3.IntegrityError as e:
        print("Integrity error occurred. IntegrityError:", e)

# Call the create_activity function to insert the activities into the table
create_activity('bodybuilding')
create_activity('crossfit')
create_activity('mixed_arts')

