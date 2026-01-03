import streamlit as st
import pandas as pd

# --- 1. MEMORY SETUP ---
# If these aren't here, the report button WILL NOT work.
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = []
if 'audit_run' not in st.session_state:
    st.session_state.audit_run = False

st.title("LogiShield AI Auditor")

# --- 2. THE FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload Manifest", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- 3. THE PROCESSING BUTTON ---
    if st.button("🚀 Start AI Audit"):
        temp_results = []
        
        # This is your main loop
        for index, row in df.iterrows():
            # (Your HTS Logic here)
            # Example of what we are saving:
            temp_results.append({
                "index": index,
                "hscode": row.get('HTS', 'Unknown'),
                "status": "Critical", 
                "issue": "Needs 2026 Verification",
                "remedy": "Reclassify to 8501.10"
            })
        
        # SAVE TO MEMORY so the next button can see it
        st.session_state.audit_results = temp_results
        st.session_state.audit_run = True
        st.success("Audit Completed!")

# --- 4. THE REPORT BUTTON (Outside the loop!) ---
# This checks if 'audit_run' is True in memory
if st.session_state.audit_run:
    st.divider()
    
    if st.button("📊 Show Full Report"):
        st.subheader("Final Audit Results")
        
        # Display the data from memory
        for item in st.session_state.audit_results:
            with st.expander(f"Row {item['index']}: {item['hscode']}"):
                st.write(f"**Risk:** {item['status']}")
                st.info(f"**Advice:** {item['remedy']}")

        # Download option
        report_df = pd.DataFrame(st.session_state.audit_results)
        st.download_button("Download CSV", report_df.to_csv(), "report.csv")
        if st.button("Test Database Connection"):
    # 1. Prepare a small piece of data
    test_data = {
        "filename": "test_manifest.csv",
        "findings": {"status": "Connected", "message": "It works!"}
    }
    
    # 2. Send it to your table
    try:
        response = supabase.table("audit_history").insert(test_data).execute()
        st.success("🚀 Data appeared in Supabase! Check your dashboard.")
    except Exception as e:
        st.error(f"Failed to send data: {e}")

