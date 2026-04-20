import os
import pandas as pd

def init_rlhf_db():
    if not os.path.exists("rlhf_dataset.csv"):
        df = pd.DataFrame(columns=["claim_id", "decision", "confidence_score", "human_feedback", "reward_value"])
        df.to_csv("rlhf_dataset.csv", index=False)

def log_adjuster_feedback(claim_id, decision, confidence, feedback_type):
    """Human-in-the-loop Reward Logging"""
    reward = 1.0 if feedback_type == "Upvote" else -1.0
    
    new_data = pd.DataFrame([{
        "claim_id": claim_id,
        "decision": decision,
        "confidence_score": confidence,
        "human_feedback": feedback_type,
        "reward_value": reward
    }])
    
    new_data.to_csv("rlhf_dataset.csv", mode='a', header=False, index=False)
    return reward
