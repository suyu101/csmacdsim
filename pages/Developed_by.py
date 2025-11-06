import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Developed By",
    page_icon="👥",
    layout="wide"
)

# Sidebar navigation links (from your code)
st.sidebar.page_link('Home.py', label='Home')
st.sidebar.page_link('pages/CSMA_CD.py', label='CSMA/CD')
st.sidebar.page_link('pages/Slotted_Aloha.py', label='Slotted_Aloha')
st.sidebar.markdown("---")

# Custom CSS for the header
st.markdown("""
<style>
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

st.divider()

# Navigation Bar (from your code)
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
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
with col5:
    # Set this as 'primary' to show it's the active page
    if st.button("Developed by", use_container_width=True, type="primary"):
        st.switch_page("pages/Developed_by.py")

st.divider()

# Header Section (from your code)
st.markdown("""
<div class="page-header">
    <h1>Developed By</h1>
</div>
""", unsafe_allow_html=True)

# --- START: FIXED SECTION ---

st.markdown("## 👥 Project Team Members")

team_members = [
    {"name": "Katyayni Aarya", "reg_no": "24BCE1543", "photo": "images/p1.jpg"},
    {"name": "Suyesha Saha", "reg_no": "24BCE1962", "photo": "images/p2.jpg"}
]

# Loop through each member and create a container with columns
for member in team_members:
    # Use a bordered container to create a "card" effect
    with st.container(border=True):
        # Create columns: 1 part for image, 3 parts for text
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # FIX: Call st.image() directly
            # Make sure the path 'images/p1.jpg' is correct!
            try:
                st.image(member['photo'], width=150)
            except Exception as e:
                st.error(f"Could not load image: {member['photo']}")
                st.caption("Please check the file path.")

        with col2:
            # FIX: Use standard streamlit elements for text
            st.subheader(member['name'])
            st.markdown(f"**Registration No:** {member['reg_no']}")
    
    st.write("") # Adds a little vertical space between members

st.divider()

# --- ADDED: GUIDE SECTION ---

st.markdown("## 🧑‍🏫 Project Guide")

# Update this with your guide's information
guide_info = {
    "name": "Dr. Guide Name",
    "title": "Professor, School of Computer Science",
    "photo": "images/p2.jpg" # Make sure this path is correct
}

with st.container(border=True):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            st.image(guide_info['photo'], width=150)
        except Exception as e:
            st.error(f"Could not load image: {guide_info['photo']}")
            st.caption("Please check the file path.")
    
    with col2:
        st.subheader(guide_info['name'])
        st.markdown(f"**{guide_info['title']}**")