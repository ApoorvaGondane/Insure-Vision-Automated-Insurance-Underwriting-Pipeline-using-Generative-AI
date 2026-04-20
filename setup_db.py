import sqlite3

def init_db():
    conn = sqlite3.connect('insurance_data.db')
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS policies (
        user_id TEXT PRIMARY KEY, policy_id TEXT, coverage TEXT, 
        limit_amt INTEGER, deductible INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS driver_history (
        user_id TEXT PRIMARY KEY, claims_last_5_years INTEGER, 
        risk_score INTEGER, risk_category TEXT)''')

    # --- Test Case Data ---
    # 1. The Standard Case (USR123): Low risk, enough coverage.
    # 2. The Over-Limit Case (USR456): Low risk, but damage (e.g. $2500) exceeds tiny limit.
    # 3. The High-Risk Case (USR789): High claims history, should trigger caution.
    # 4. The Premium Case (USR001): High limits, zero risk.
    # 5. The Luxury Case (USR999): High deductible, specialized coverage.

    policies = [
        ('USR123', 'POL-8829', 'Collision', 5000, 500),
        ('USR456', 'POL-1001', 'Basic', 1000, 200),
        ('USR789', 'POL-5502', 'Collision', 10000, 1000),
        ('USR001', 'POL-0001', 'Platinum', 50000, 0),
        ('USR999', 'POL-9999', 'Luxury', 25000, 5000)
    ]

    history = [
        ('USR123', 0, 12, 'LOW'),
        ('USR456', 0, 5, 'LOW'),
        ('USR789', 4, 88, 'HIGH'),
        ('USR001', 0, 2, 'LOW'),
        ('USR999', 1, 45, 'MEDIUM')
    ]

    # Bulk Insert
    cursor.executemany("INSERT OR REPLACE INTO policies VALUES (?, ?, ?, ?, ?)", policies)
    cursor.executemany("INSERT OR REPLACE INTO driver_history VALUES (?, ?, ?, ?)", history)
    
    conn.commit()
    conn.close()
    print(f"Database Initialized with {len(policies)} test users.")

if __name__ == "__main__":
    init_db()