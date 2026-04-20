import time
from database_service import fetch_insurance_policy, query_driver_history

def execute_reasoning_loop(vlm_finding, user_id):
    """
    Dynamic Chain-of-Thought & ReAct Framework.
    The reasoning now changes based on the data retrieved for the specific user_id.
    """
    trace = []
    risk = "NOT_EVALUATED" 
    status = "PENDING"
    payout = 0
    limit = 0
    
    # --- Step 1: Policy Retrieval ---
    trace.append(("🤔 Reason", f"I see '{vlm_finding['finding']}' in the parsed VLM output. Fetching policy for {user_id}."))
    
    trace.append(("🛠️ Action", f"Call Tool `API_Fetch_Policy(user_id='{user_id}')`"))
    policy = fetch_insurance_policy(user_id)
    
    if "error" in policy:
        return [("❌ Error", f"Policy not found for {user_id}")], {"status": "DENIED", "reason": "No active policy."}

    trace.append(("📄 Observation (RAG)", f"Policy limit: ${policy['limit_amt']}, Deductible: ${policy['deductible']}."))

    # --- Step 2: Policy Reasoning ---
    estimated_cost = vlm_finding['estimated_cost']
    limit = policy['limit_amt']
    
    if estimated_cost > limit:
        reasoning = f"The damage (${estimated_cost}) exceeds the policy limit (${limit})."
        trace.append(("🤔 Reason", reasoning))
        status = "REJECTED"
        payout = 0
    else:
        trace.append(("🤔 Reason", f"The damage (${estimated_cost}) is within policy limits. Checking driver risk profile."))
        
        # --- Step 3: Risk Assessment ---
        trace.append(("🛠️ Action", f"Call Tool `SQL_Query_Driver_History(user_id='{user_id}')`"))
        history = query_driver_history(user_id)
        
        risk = history['risk_category']
        trace.append(("📊 Observation (SQL)", f"Risk Score: {history['risk_score']} ({risk}). Claims: {history['claims_last_5_years']}."))

        if risk == "HIGH":
            trace.append(("✅ Reason", "Claim flagged for manual audit due to High Driver Risk."))
            status = "FLAGGED FOR REVIEW"
            payout = 0
        else:
            trace.append(("✅ Reason", "Low risk driver and valid coverage. Approving claim."))
            status = "APPROVED"
            payout = max(0, estimated_cost - policy['deductible'])

    # --- Step 4: Final Output ---
    final_decision = {
        "user_id": user_id,
        "status": status,
        "confidence_score": 0.94,
        "estimated_payout": f"${payout}",
        "reasoning_summary": f"Processed via ReAct loop for {user_id}. Outcome based on {risk} risk and ${limit} limit."
    }
    
    return trace, final_decision
