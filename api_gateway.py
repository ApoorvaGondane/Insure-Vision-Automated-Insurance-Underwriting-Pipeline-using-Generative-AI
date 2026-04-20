import random
from vlm_service import process_image_with_vlm
from react_agent import execute_reasoning_loop

def process_claim_request(image_file, user_id):
    """
    API Gateway: Orchestrates the microservices.
    Now accepts user_id to enable dynamic RAG and DB lookups.
    """
    claim_id = f"CLM-{random.randint(1000, 9999)}"
    
    # Route 1: Vision Model (The Perception Layer)
    vlm_result = process_image_with_vlm(image_file)
    print(vlm_result)
    if vlm_result.get("status") == "error":
        return vlm_result, [], {"status": "FAILED", "error": "VLM Processing failed"}

    # Route 2: ReAct Agent (The Reasoning Layer)
    # We pass BOTH the VLM findings and the specific user_id
    trace, final_decision = execute_reasoning_loop(vlm_result, user_id)
    
    # Attach Metadata
    final_decision["claim_id"] = claim_id
    final_decision["processed_by"] = "InsureVision-Gateway-v2"
    
    return vlm_result, trace, final_decision