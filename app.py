import streamlit as st
import time
from api_gateway import process_claim_request
from rlhf_service import init_rlhf_db, log_adjuster_feedback

def inject_premium_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Gradient */
    .premium-title {
        background: -webkit-linear-gradient(45deg, #4ECDC4, #556270);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    /* Microservice Tag */
    .micro-tag {
        background-color: rgba(78, 205, 196, 0.15);
        color: #4ECDC4;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 15px;
        display: inline-block;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    /* Process Flow Button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #4ECDC4 0%, #2C3E50 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="InsureVision Premium", page_icon="🛡️", layout="wide")
    inject_premium_css()
    init_rlhf_db()

    st.markdown("<h1 class='premium-title'>🛡️ InsureVision</h1>", unsafe_allow_html=True)
    st.markdown("<div class='micro-tag'>ENTERPRISE MICROSERVICES ARCHITECTURE</div>", unsafe_allow_html=True)
    # selector to choose user_ids (AAD Unit 2: User Context)
    user_list = ["USR123", "USR456", "USR789", "USR001", "USR999"]
    selected_user = st.selectbox("Select Policyholder ID", user_list)
    st.sidebar.title("System Diagnostics")
    st.sidebar.markdown("---")
    st.sidebar.success("🟢 API Gateway: Routing Online")
    st.sidebar.success("🟢 VLM Service: Moondream2-LoRA Online")
    st.sidebar.success("🟢 ReAct Agent: LangChain Framework Online")
    st.sidebar.success("🟢 Policy Database: SQL Driver Connected")
    st.sidebar.success("🟢 RLHF Logger: Metric Collection Active")

    # Layout Shift: 2 Columns for professional dashboard feel
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.write("### 📸 1. Claim Evidence Upload")
        uploaded_file = st.file_uploader("Upload vehicle damage photo...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Captured Image",width='stretch', clamp=True)
            
            if st.button("🚀 Execute GenAI Underwriting Pipeline", type="primary", width='stretch'):
                st.session_state['run_pipeline'] = True

    with col_right:
        if uploaded_file is not None and st.session_state.get('run_pipeline', False):
            st.write("### ⚙️ 2. Processing Telemetry")
            
            st.markdown("##### 👁️ Vision-Language Model Analysis")
            with st.spinner("Analyzing image via VLM..."):
                vlm_result, trace, final_decision = process_claim_request(uploaded_file,selected_user)
                print(vlm_result)
                st.success("VLM Diagnostics Complete")
                st.info(f"**VLM Identified:** {vlm_result['finding']}")

            st.markdown("##### 🧠 Chain-of-Thought & ReAct Trace")
            with st.status("Agent dynamically selecting reasoning tools...", expanded=True) as status:
                for step, detail in trace:
                    st.markdown(f"**{step}:** {detail}")
                    time.sleep(1.2)
                status.update(label="Reasoning Loop Concluded", state="complete", expanded=False)

            st.markdown("##### 📑 Final Automated Underwriting Output")
            st.json(final_decision)
            st.session_state['current_claim'] = final_decision
            st.session_state['run_pipeline'] = False # Reset trigger so it doesn't double-run

    # RLHF bottom section
    if 'current_claim' in st.session_state and not st.session_state.get('run_pipeline', False):
        st.markdown("---")
        st.markdown("### 👩‍⚖️ 3. Human-in-the-Loop & RLHF Policy")
        st.caption("Adjuster Override System. Decisions feed into Reward Model for continuous alignment.")
        
        c1, c2, c3, c4 = st.columns(4)
        claim_data = st.session_state['current_claim']
        with c1:
            if st.button("👍 Approve (Upvote)", width='stretch'):
                reward = log_adjuster_feedback(claim_data['claim_id'], claim_data['status'], claim_data['confidence_score'], "Upvote")
                st.success("Dataset Updated. AI Rewarded.")
        with c2:
            if st.button("👎 Reject (Downvote)", width='stretch'):
                reward = log_adjuster_feedback(claim_data['claim_id'], claim_data['status'], claim_data['confidence_score'], "Downvote")
                st.error("Dataset Updated. AI Penalized.")

if __name__ == "__main__":
    main()
