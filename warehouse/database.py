import sqlite3
from datetime import datetime,timedelta

current_date = datetime.now()

## this function will create member within members table 
def create_member(**kwargs):
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




#? this function will be called for new GYM subscriber(remaining_session(monthly=None,20_session=20,30_session=30))
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
                #!------------extend for another month-----------------
                new_end_date = datetime.now() + timedelta(days=30)
                cursor.execute(
                    "UPDATE subscriptions SET subscription_end_date=? WHERE member_id=? AND activity_id=?", 
                    (new_end_date.strftime("%Y-%m-%d"), member_id, activity_id)
                )
                #!------------extend for another month-----------------
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


# update_member_entry('824518f0-653e-4153-b9ea-9d9bcae8337a')


#! Funtion to write into user_hmac table and we will call it into the encode function ([./utils/encod_decod_QR.py]) 
def insert_user_hmac(member_id,encoded_data):
    sql_statment = "INSERT INTO user_hmac (member_id, HMAC) VALUES (?, ?)"
    try:
        with sqlite3.connect('warehouse.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statment,(member_id,encoded_data))
            conn.commit()
    except sqlite3.OperationalError as err:
        print("Error ",err)
    finally:
        conn.close()
        