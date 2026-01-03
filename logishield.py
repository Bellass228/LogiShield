# --- 1. LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")

def logout_user():
    supabase.auth.sign_out()
    st.session_state.logged_in = False
    st.rerun()

# --- 2. THE UI GATEKEEPER ---
if not st.session_state.logged_in:
    st.title("🔐 LogiShield Secure Access")
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login_user(email, password)
            
    with tab2:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            try:
                supabase.auth.sign_up({"email": new_email, "password": new_password})
                st.success("Account created! You can now login.")
            except Exception as e:
                st.error(f"Registration failed: {e}")
    st.stop() # Stops the rest of the app from running until logged in
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
        st.sidebar.write(f"Logged in as: {st.session_state.user_email}")
if st.sidebar.button("Logout"):
    logout_user()

