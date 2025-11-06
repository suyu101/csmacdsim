import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Developed By",
    page_icon="👥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .member-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        margin: 1rem 0;
    }
    .member-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .photo-placeholder {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: white;
    }
    .member-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin: 0.5rem 0;
    }
    .member-reg {
        font-size: 1.1rem;
        color: #666;
        margin: 0.5rem 0;
    }
    .page-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1.5])

with col1:
    if st.button("Home", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    if st.button("Download", use_container_width=True):
        st.switch_page("pages/Download.py")

with col3:
    if st.button("Help", use_container_width=True):
        st.switch_page("pages/Help.py")

with col4:
    if st.button("Learn", use_container_width=True):
        st.switch_page("pages/Learn.py")

st.divider()

# Header
st.markdown("""
<div class="page-header">
    <h1>👥 Developed By</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Meet the Team Behind This Project
    </p>
</div>
""", unsafe_allow_html=True)

# Team Members Section
st.markdown("## 👨‍💻 Project Team Members")

# You can customize this - add as many members as needed
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="member-card">
        <div class="photo-placeholder">👤</div>
        <div class="member-name">Your Name</div>
        <div class="member-reg">Reg No: XXXXXXXX</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button to upload photo (optional)
    if st.button("📸 Upload Photo", key="photo1"):
        st.info("Photo upload functionality - Add your photo here")

with col2:
    st.markdown("""
    <div class="member-card">
        <div class="photo-placeholder">👤</div>
        <div class="member-name">Team Member 2</div>
        <div class="member-reg">Reg No: XXXXXXXX</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📸 Upload Photo", key="photo2"):
        st.info("Photo upload functionality - Add your photo here")

st.divider()

# Add yourself section
st.markdown("## ➕ Add Team Member")

with st.expander("Click to add your information"):
    name = st.text_input("Your Name", placeholder="Enter your full name")
    reg_no = st.text_input("Registration Number", placeholder="Enter your registration number")
    role = st.text_input("Role in Project", placeholder="e.g., Developer, Designer, Researcher")
    
    if st.button("Add Member", type="primary"):
        if name and reg_no:
            st.success(f"Added {name} - {reg_no} to the team!")
        else:
            st.error("Please fill in all required fields")

st.divider()

# Project Information
st.markdown("## 📋 Project Information")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    ### Project Details
    - **Course**: Computer Networks
    - **Project**: Network Protocol Simulator
    - **Protocols Implemented**: 
        - CSMA/CD (with variants)
        - Slotted ALOHA
    - **Technologies Used**: 
        - Python
        - Streamlit
        - NumPy
        - Matplotlib
        - Pandas
    """)

with col_b:
    st.markdown("""
    ### Features Implemented
    - ✅ Interactive protocol simulations
    - ✅ Real-time visualization
    - ✅ Performance metrics
    - ✅ Gantt timeline charts
    - ✅ Data export (CSV)
    - ✅ Protocol comparison
    - ✅ Educational content
    """)

st.divider()

# Acknowledgments
st.markdown("## 🙏 Acknowledgments")

st.markdown("""
We would like to express our gratitude to:
- Our course instructor for guidance and support
- Our university for providing the resources
- The open-source community for amazing tools and libraries
""")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 0.9rem; color: #666;">
        Network Protocol Simulator | Computer Networks Project<br>
        © 2024 All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)