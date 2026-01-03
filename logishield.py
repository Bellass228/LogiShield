
import json

# Simulated "Knowledge Base" of 2025 Trade Regulations
TRADE_REGS = {
    "SHIPPING_CODE_8542": {"item": "Microchips", "restriction": "High", "license_required": True},
    "SHIPPING_CODE_2204": {"item": "Wine", "restriction": "Moderate", "tax_rate": 0.15},
}

def audit_manifest(manifest_data):
    print("--- LogiShield AI: Audit Initializing ---")
    results = {"status": "Clear", "flags": [], "estimated_tax": 0}
    
    for item in manifest_data['items']:
        code = item['hscode']
        
        # 1. Check for Regulation Match
        if code in TRADE_REGS:
            reg = TRADE_REGS[code]
            print(f"Checking {reg['item']}...")
            
            # 2. Logic: Check for Missing Licenses
            if reg['restriction'] == "High" and not item.get('has_license'):
                results['status'] = "FLAGGED"
                results['flags'].append(f"CRITICAL: Missing export license for {reg['item']}")
            
            # 3. Logic: Calculate Tax Exposure
            if 'tax_rate' in reg:
                tax = item['value'] * reg['tax_rate']
                results['estimated_tax'] += tax
        else:
            results['status'] = "FLAGGED"
            results['flags'].append(f"UNKNOWN CODE: {code} requires manual review.")
            
    return results

# --- TEST CASE ---
sample_manifest = {
    "shipment_id": "EXP-2025-99",
    "items": [
        {"hscode": "8542", "value": 50000, "has_license": False}, # This should trigger a flag
        {"hscode": "2204", "value": 12000}
    ]
}

audit_report = audit_manifest(sample_manifest)
print(f"\nFINAL REPORT:\n{json.dumps(audit_report, indent=2)}")
import streamlit as st
import pandas as pd
import json

# --- Page Config ---
st.set_page_config(page_title="LogiShield AI | Compliance Dashboard", layout="wide")

st.title("🛡️ LogiShield AI")
st.subheader("Global Trade Compliance & Risk Audit")

# --- Sidebar: Industry Rules ---
st.sidebar.header("Regulation Settings")
industry = st.sidebar.selectbox("Select Niche", ["Wine & Spirits", "Pharmaceuticals", "Electronics"])
strictness = st.sidebar.slider("Audit Sensitivity", 0, 100, 85)

# --- Main Interface ---
st.write(f"### Active Audit: {industry}")

# Upload Section
uploaded_file = st.file_uploader("Upload Shipping Manifest (JSON/CSV)", type=['json', 'csv'])

# Mock Data for Demonstration
if uploaded_file is None:
    st.info("Please upload a file or use the sample manifest below.")
    sample_data = [
        {"Item": "Chardonnay Case", "HS_Code": "2204", "Value": 15000, "Origin": "France", "Destination": "USA"},
        {"Item": "Lithium Batteries", "HS_Code": "8506", "Value": 2500, "Origin": "China", "Destination": "USA"}
    ]
    df = pd.DataFrame(sample_data)
else:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_json(uploaded_file)

# Display the Data
st.dataframe(df, use_container_width=True)

# --- The AI Audit Logic (Visualized) ---
if st.button("Run LogiShield Audit"):
    with st.spinner('Analyzing against 2025 Trade Regulations...'):
        # Simulated logic
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        # Key Metrics
        col1.metric("Compliance Score", "92%", "-8%")
        col2.metric("Estimated Duties", "$2,250", "+$150")
        col3.metric("Risk Level", "MODERATE", delta_color="inverse")
        
        # Detailed Flags
        st.write("### 🚩 Risk Findings")
        for index, row in df.iterrows():
            if row['HS_Code'] == "8506":
                st.error(f"**Item {index+1}: {row['Item']}** - WARNING: Missing UN38.3 Safety Certification for Lithium transport.")
            if row['Origin'] == "China" and industry == "Electronics":
                st.warning(f"**Item {index+1}: {row['Item']}** - Section 301 Tariff alert: Additional 25% duty may apply.")

st.sidebar.markdown("---")
st.sidebar.write("**LogiShield Alpha v1.0**")
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
    import streamlit as st
import pandas as pd

# Assume 'audit_results' is a list of dictionaries you created during the loop
# audit_results = [{"item": "8506", "status": "Critical", "issue": "Lithium Battery"}, ...]

st.divider() # Visual break

if st.button("📊 Generate Final Audit Report", type="primary"):
    st.subheader("LogiShield Compliance Summary")
    
    # 1. High-Level Stats (The "Billionaire" Dashboard look)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items", len(df))
    col2.metric("Critical Risks", "4", delta="-2 vs last week", delta_color="inverse")
    col3.metric("Estimated Duties", "$12,450", delta="Saved $1.2k")
    st.write("### Detailed Risk Analysis")
    
    for item in audit_results: # pyright: ignore[reportUndefinedVariable]
        # Dynamic color based on risk
        icon = "🚩" if item['status'] == "Critical" else "⚠️"
        
        with st.expander(f"{icon} Row {item['index']}: {item['hscode']} - {item['status']}"):
            st.write(f"**Issue:** {item['issue']}")
            st.info(f"**Recommended Action:** {item['remedy']}")
            
    
            if st.button(f"Mark Row {item['index']} as Resolved", key=f"btn_{item['index']}"):
                st.success("Issue resolved in database.")

    st.download_button(
        label="📥 Download Formal Report (CSV)",
        data=pd.DataFrame(audit_results).to_csv(index=False),  # pyright: ignore[reportUndefinedVariable]
        file_name="LogiShield_Audit_Report.csv",
        mime="text/csv"
    )
import streamlit as st
import pandas as pd

if 'audit_results' not in st.session_state:
    st.session_state.audit_results = []
if 'audit_complete' not in st.session_state:
    st.session_state.audit_complete = False


# st.session_state.audit_results = your_loop_results
# st.session_state.audit_complete = True

st.divider() 


if st.session_state.audit_complete:
    
    if st.button("📊 Generate Final Audit Report", type="primary") or st.session_state.get('report_visible', False):
        # Keep the report visible even if other buttons are clicked
        st.session_state.report_visible = True
        
        st.subheader("LogiShield Compliance Summary")
    
        # High-Level Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Items", len(st.session_state.audit_results))
        col2.metric("Critical Risks", "4", delta="-2 vs last week", delta_color="inverse")
        col3.metric("Estimated Duties", "$12,450", delta="Saved $1.2k")
        
        st.write("### Detailed Risk Analysis")
    
        # Use session_state.audit_results instead of a local variable
        for item in st.session_state.audit_results:
            icon = "🚩" if item['status'] == "Critical" else "⚠️"
            
            with st.expander(f"{icon} Row {item['index']}: {item['hscode']} - {item['status']}"):
                st.write(f"**Issue:** {item['issue']}")
                st.info(f"**Recommended Action:** {item['remedy']}")
                
                # UNIQUE KEYS: Every button in a loop needs a unique key
                if st.button(f"Mark Row {item['index']} as Resolved", key=f"resolve_{item['index']}"):
                    st.success(f"Row {item['index']} marked as resolved!")

        # Download button uses the saved state data
        report_df = pd.DataFrame(st.session_state.audit_results)
        st.download_button(
            label="📥 Download Formal Report (CSV)",
            data=report_df.to_csv(index=False),
            file_name="LogiShield_Audit_Report.csv",
            mime="text/csv"
        )
else:
    st.info("Please run the audit above to generate the report.")
