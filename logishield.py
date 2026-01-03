import streamlit as st
import pandas as pd
from supabase import create_client # New Import

# --- 1. CONNECTION SETUP (TOP) ---
# This uses the secrets you just fixed!
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- 2. MEMORY SETUP ---
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = []
if 'audit_run' not in st.session_state:
    st.session_state.audit_run = False

st.title("LogiShield AI Auditor")

# --- 3. THE FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload Manifest", type=['csv', 'xlsx'])

if uploaded_file:
    # Use st.cache_data so it doesn't re-read the file every time you click a button
    df = pd.read_csv(uploaded_file)
    
    if st.button("🚀 Start AI Audit"):
        temp_results = []
        for index, row in df.iterrows():
            # Your HTS Logic/Gemini call would happen here
            temp_results.append({
                "index": index,
                "hscode": row.get('HTS', 'Unknown'),
                "status": "Critical", 
                "issue": "Needs 2026 Verification",
                "remedy": "Reclassify to 8501.10"
            })
        
        st.session_state.audit_results = temp_results
        st.session_state.audit_run = True
        st.success("Audit Completed!")

# --- 4. THE REPORT & SAVE BUTTON (BOTTOM) ---
if st.session_state.audit_run:
    st.divider()
    
    # We use an OR here so the report stays open if they click "Download"
    if st.button("📊 Show Full Report & Save to History"):
        st.subheader("Final Audit Results")
        
        # --- NEW: SAVE TO SUPABASE ---
        try:
            data_to_save = {
                "filename": uploaded_file.name,
                "findings": st.session_state.audit_results 
            }
            supabase.table("audit_history").insert(data_to_save).execute()
            st.toast("✅ Saved to Cloud History!")
        except Exception as e:
            st.error(f"Cloud Save Failed: {e}")

        # Display UI
        for item in st.session_state.audit_results:
            with st.expander(f"Row {item['index']}: {item['hscode']}"):
                st.write(f"**Risk:** {item['status']}")
                st.info(f"**Advice:** {item['remedy']}")

        report_df = pd.DataFrame(st.session_state.audit_results)
        st.download_button("📥 Download CSV", report_df.to_csv(index=False), "report.csv")
