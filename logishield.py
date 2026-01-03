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
