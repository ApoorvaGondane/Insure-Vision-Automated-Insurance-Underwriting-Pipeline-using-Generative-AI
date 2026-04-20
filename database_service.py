import sqlite3

def get_data(table, user_id):
    conn = sqlite3.connect('insurance_data.db')
    conn.row_factory = sqlite3.Row
    result = conn.execute(f"SELECT * FROM {table} WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(result) if result else None

def fetch_insurance_policy(user_id):
    data = get_data('policies', user_id)
    return data if data else {"error": "No Policy Found"}

def query_driver_history(user_id):
    data = get_data('driver_history', user_id)
    return data if data else {"risk_category": "UNKNOWN"}
