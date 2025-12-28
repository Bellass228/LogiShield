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

# 1. Load the Data
uploaded_file = st.file_uploader("Upload Shipping Manifest (JSON/CSV)", type=['json', 'csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())

    # 2. THE MAPPING STEP (Before the row loop)
    # This creates a dropdown so you can select which column is the 'HS Code'
    st.write("### Configure Audit")
    target_column = st.selectbox("Which column contains the HTS/Product Code?", df.columns)

    if st.button("Run LogiShield Audit"):
        st.write("### 🚩 Risk Findings")
        
        # 3. THE ROW LOOP (Now safe from KeyError)
        for index, row in df.iterrows():
            # Use the dynamically selected column name
            current_value = str(row[target_column])
            
            if "8506" in current_value:
                st.error(f"**Item {index+1}** - WARNING: Lithium Battery detected. Check safety certs.")
            
            # Example: Check if the value is missing
            if pd.isna(row[target_column]):
                st.warning(f"**Item {index+1}** - Missing product code.")

st.info("Mapping columns before the loop prevents the 'KeyError' you encountered.")

