import sqlite3
from uuid import uuid4
from datetime import datetime,timedelta

#############user info##############
current_date = datetime.now()

user_info = {
    "member_id" : str(uuid4()),
    "username" : "adib ben haddada",
    "age": 28,
    "email":"adibbh@gmail.com",
    "entry_date" : current_date.strftime('%Y/%m/%d'),
    "activity" : "bodybuilding",
    "subscription_method" : "monthly"
}

user_info2 = {
    "member_id" : str(uuid4()),
    "username" : "skandar ben haddada",
    "age": 18,
    "email":"skon@outlook.com",
    "entry_date" : current_date.strftime('%Y/%m/%d'),
    "activity" : "crossfit",
    "subscription_method" : "20_session"
}
#####################################

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

try:
    with sqlite3.connect('warehouse.db') as conn:
        cursor = conn.cursor()

        # execute statements
        for statement in tables_statment:
            cursor.execute(statement)
        
        conn.commit()  # Commit changes
        print('Tables created successfully.')
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)


##! this function will be called in case the gym will add new activity
def create_activity(activity):
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()
            # Correct SQL query
            cursor.execute('''INSERT INTO activities(name) VALUES(?)''', (activity,))
            conn.commit()
            print(f"Successfully inserted activity: {activity}")
    except sqlite3.OperationalError as e:
        print("Failed to insert activity into database. OperationalError:", e)
    except sqlite3.IntegrityError as e:
        print("Integrity error occurred. IntegrityError:", e)
    finally:
        conn.close()


# create_activity('bodybuilding')
# create_activity('crossfit')
# create_activity('mixed_arts')


## this function will create member within members table 

def create_member(**kwargs):
    #print(kwargs)
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO members (user_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (kwargs['user_id'],kwargs['name'],kwargs["age"],kwargs["email"]))
            conn.commit()  # Commit the transaction
            print("User data inserted successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to insert data into db:", e)
    except sqlite3.IntegrityError as e:
        print("Integrity error occurred:", e)
    finally:
        conn.close()


# create_member(user_id=user_info["member_id"],name=user_info['username'],age=user_info['age'],email=user_info['email'])
# create_member(user_id=user_info2["member_id"],name=user_info2['username'],age=user_info2['age'],email=user_info2['email'])




#? this function will be called for new GYM subscriber
def create_new_subscription(**kwargs):
    activity_id = None
    query_to_fetch_activity_id = "SELECT id FROM activities WHERE name = ?"
    activity = kwargs["activity"]
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query_to_fetch_activity_id,(activity,))
            activity_id = cursor.fetchone()
            cursor.execute('''
                INSERT INTO subscriptions (
                    member_id, activity_id, subscription_method, 
                    subscription_start_date, subscription_end_date, remaining_sessions
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                kwargs["member_id"], activity_id[0], kwargs["subscription_method"],
                kwargs["subscription_start_dt"], kwargs["subscription_end_dt"], kwargs["remaining_sessions"]
            ))
            conn.commit()
            print("Subscription added successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to insert subscription into database:", e)
    except sqlite3.IntegrityError as e:
        print("Integrity error occurred:", e)
    finally:
        conn.close()


## we gonna replace this variable from here
subscription_start_date = datetime.strptime(user_info["entry_date"], '%Y/%m/%d')
subscription_end_date = subscription_start_date + timedelta(days=30)


# create_new_subscription(member_id=user_info['member_id'],
#                         subscription_method=user_info["subscription_method"],
#                         subscription_start_dt=subscription_start_date.strftime('%Y-%m-%d'),subscription_end_dt=subscription_end_date.strftime('%Y-%m-%d'),
#                         remaining_sessions=None,activity=user_info["activity"])


# create_new_subscription(member_id=user_info2['member_id'],
#                         subscription_method=user_info2["subscription_method"],
#                         subscription_start_dt=subscription_start_date.strftime('%Y-%m-%d'),subscription_end_dt=None,
#                         remaining_sessions=20,activity=user_info2["activity"])






###!this function will be used in resubscription


def update_member_entry(member_id):
    # Enable column-based access for better readability
    conn = sqlite3.connect("warehouse.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch all subscriptions for the member
    cursor.execute("SELECT * FROM subscriptions WHERE member_id=?", (member_id,))
    subscriptions = cursor.fetchall()

    if not subscriptions:
        print("No active subscription found for the member.")
        return

    for subscription in subscriptions:
        subscription_method = subscription["subscription_method"]  # 'monthly' or '20_session'/'30_session'
        activity_id = subscription["activity_id"]  # Which activity the subscription applies to

        if subscription_method == 'monthly':
            subscription_end_date = datetime.strptime(subscription["subscription_end_date"], "%Y-%m-%d")
            
            if datetime.now() > subscription_end_date:
                print("Monthly subscription expired. Extending for another month.")
                new_end_date = datetime.now() + timedelta(days=30)
                cursor.execute(
                    "UPDATE subscriptions SET subscription_end_date=? WHERE member_id=? AND activity_id=?", 
                    (new_end_date.strftime("%Y-%m-%d"), member_id, activity_id)
                )
            else:
                print("Monthly subscription still active.")
        
        elif subscription_method in ('20_session', '30_session'):
            remaining_sessions = subscription["remaining_sessions"]
            
            if remaining_sessions > 0:
                remaining_sessions -= 1
                cursor.execute(
                    "UPDATE subscriptions SET remaining_sessions=? WHERE member_id=? AND activity_id=?", 
                    (remaining_sessions, member_id, activity_id)
                )
                if remaining_sessions == 0:
                    print("Session-based subscription used up. Please renew.")
            else:
                print("No remaining sessions. Entry not allowed.")
                continue  # Skip transaction logging for this subscription

        # Log the visit in the transactions table
        cursor.execute(
            "INSERT INTO transactions (member_id, visit_date, activity_id) VALUES (?, ?, ?)", 
            (member_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), activity_id)
        )

    conn.commit()
    conn.close()


update_member_entry('824518f0-653e-4153-b9ea-9d9bcae8337a')
