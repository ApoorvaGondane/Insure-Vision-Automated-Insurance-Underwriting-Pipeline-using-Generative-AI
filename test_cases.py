from database_service import fetch_insurance_policy, query_driver_history

test_users = ['USR123', 'USR456', 'USR789']

for user in test_users:
    print(f"\n--- Testing User: {user} ---")
    print(f"Policy: {fetch_insurance_policy(user)['limit_amt']}")
    print(f"Risk: {query_driver_history(user)['risk_category']}")