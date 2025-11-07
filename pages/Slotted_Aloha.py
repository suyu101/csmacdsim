import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io

# Page configuration
st.set_page_config(
    page_title="Slotted ALOHA Simulator",
    page_icon="📡",
    layout="wide"
)
st.sidebar.page_link('Home.py', label='Home')
st.sidebar.page_link('pages/CSMA_CD.py', label='CSMA/CD')
st.sidebar.page_link('pages/Slotted_Aloha.py', label='Slotted_Aloha')
st.sidebar.markdown("---")

st.divider()
# Navigation Bar
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
    if st.button("Developed by", use_container_width=True):
        st.switch_page("pages/Developed_by.py")

st.divider()

# Title and description
st.title("Slotted ALOHA Protocol Simulator")
st.markdown("""
This simulator demonstrates the **Slotted ALOHA** protocol, a random access protocol 
where time is divided into slots and nodes can only transmit at the beginning of a slot.
""")

# Sidebar for input controls
st.sidebar.header("Simulation Parameters")

num_nodes = st.sidebar.slider(
    "Number of Nodes",
    min_value=2,
    max_value=50,
    value=10,
    help="Number of nodes competing for channel access"
)

transmission_prob = st.sidebar.slider(
    "Transmission Probability (p)",
    min_value=0.01,
    max_value=1.0,
    value=0.3,
    step=0.01,
    help="Probability that a node will attempt to transmit in a given slot"
)

num_slots = st.sidebar.slider(
    "Number of Time Slots",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100,
    help="Total number of time slots to simulate"
)

# Run simulation button
run_simulation = st.sidebar.button("Run Simulation", type="primary")

# Slotted ALOHA simulation logic
def simulate_slotted_aloha(num_nodes, p, num_slots):
    slots_data = []
    node_transmissions = {i: [] for i in range(num_nodes)}
    successful_transmissions = 0
    collisions = 0
    idle_slots = 0

    for slot in range(num_slots):
        transmitting_nodes = np.random.random(num_nodes) < p
        num_transmissions = np.sum(transmitting_nodes)
        transmitting_node_ids = [i for i in range(num_nodes) if transmitting_nodes[i]]

        if num_transmissions == 0:
            status = "Idle"
            idle_slots += 1
            for i in range(num_nodes):
                node_transmissions[i].append((slot, 0))
        elif num_transmissions == 1:
            status = "Success"
            successful_transmissions += 1
            for i in range(num_nodes):
                if i in transmitting_node_ids:
                    node_transmissions[i].append((slot, 1))
                else:
                    node_transmissions[i].append((slot, 0))
        else:
            status = "Collision"
            collisions += 1
            for i in range(num_nodes):
                if i in transmitting_node_ids:
                    node_transmissions[i].append((slot, 2))
                else:
                    node_transmissions[i].append((slot, 0))

        slots_data.append((slot, num_transmissions, status))

    throughput = successful_transmissions / num_slots
    theoretical_max = 1 / np.e
    offered_load = num_nodes * p
    stats = {
        "successful": successful_transmissions,
        "collisions": collisions,
        "idle": idle_slots,
        "throughput": throughput,
        "theoretical_max": theoretical_max,
        "offered_load": offered_load,
        "efficiency": (throughput / theoretical_max) * 100
    }

    return slots_data, node_transmissions, stats

def get_theoretical_throughput(G_values):
    return G_values * np.exp(-G_values)

def plot_node_timeline(node_transmissions, num_slots_to_show=50):
    colors = {0: '#d3d3d3', 1: '#2ecc71', 2: '#e74c3c'}
    labels = {0: 'Idle', 1: 'Success', 2: 'Collision'}
    num_nodes = len(node_transmissions)
    display_slots = min(num_slots_to_show, len(node_transmissions[0]))
    fig, ax = plt.subplots(figsize=(14, max(6, num_nodes * 0.4)))

    for node_id, transmissions in node_transmissions.items():
        for slot, state in transmissions[:display_slots]:
            ax.barh(node_id, 1, left=slot, color=colors[state], height=0.8, edgecolor='white', linewidth=0.5)

    ax.set_xlabel('Time Slot', fontsize=12)
    ax.set_ylabel('Node ID', fontsize=12)
    ax.set_title(f'Timeline Diagram: Packet Transmission Attempts (First {display_slots} slots)', fontsize=14, fontweight='bold')
    ax.set_xlim(-0.5, display_slots)
    ax.set_ylim(-0.5, num_nodes - 0.5)
    ax.set_yticks(range(num_nodes))
    ax.set_yticklabels([f"Node {i}" for i in range(num_nodes)])
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[k], label=labels[k]) for k in sorted(labels.keys())]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

# --------------------- MAIN SIMULATION ---------------------
if run_simulation:
    with st.spinner("Running simulation..."):
        slots_data, node_transmissions, stats = simulate_slotted_aloha(num_nodes, transmission_prob, num_slots)

    st.header("Simulation Results")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Throughput (S)", f"{stats['throughput']:.4f}")
    col2.metric("Success Rate", f"{(stats['successful']/num_slots)*100:.1f}%")
    col3.metric("Collision Rate", f"{(stats['collisions']/num_slots)*100:.1f}%")
    col4.metric("Idle Rate", f"{(stats['idle']/num_slots)*100:.1f}%")

    st.divider()

    st.subheader("Slot-wise Event Table")
    df_events = pd.DataFrame(slots_data, columns=['Slot', 'Num Transmissions', 'Status'])
    st.dataframe(df_events, use_container_width=True, height=400)

    st.divider()
    st.subheader("Timeline Diagram: Packet Transmission Attempts")
    plot_node_timeline(node_transmissions, num_slots_to_show=min(100, num_slots))

    st.divider()
    st.subheader("Throughput Calculation & Efficiency Graph vs Offered Load")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        **Throughput Calculation:**  
        - Successful Transmissions: {stats['successful']}  
        - Total Slots: {num_slots}  
        - Throughput (S): {stats['throughput']:.4f}  
        - Formula: S = Successful Transmissions / Total Slots  
        - Calculation: {stats['successful']} / {num_slots} = {stats['throughput']:.4f}

        **Performance Metrics:**  
        - Offered Load (G): {stats['offered_load']:.3f}  
        - Efficiency: {stats['efficiency']:.1f}% of theoretical max  
        - Theoretical Maximum: {stats['theoretical_max']:.4f}  
        - Collisions: {stats['collisions']}  
        - Idle Slots: {stats['idle']}
        """)

    with col_b:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        G_range = np.linspace(0, 5, 100)
        S_theoretical = get_theoretical_throughput(G_range)
        ax1.plot(G_range, S_theoretical, 'b-', linewidth=2, label='Theoretical')
        ax1.plot(stats['offered_load'], stats['throughput'], 'ro', markersize=12, label=f'Simulated (G={stats["offered_load"]:.2f})')
        ax1.plot(1, 1/np.e, 'g*', markersize=15, label=f'Maximum (G=1, S={1/np.e:.3f})')
        ax1.set_xlabel('Offered Load (G = N × p)', fontsize=12)
        ax1.set_ylabel('Throughput (S)', fontsize=12)
        ax1.set_title('Efficiency Graph: Throughput vs Offered Load', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_xlim(0, 5)
        ax1.set_ylim(0, 0.4)
        st.pyplot(fig1)

    st.divider()
    st.subheader("Additional Visualizations")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sizes = [stats['successful'], stats['collisions'], stats['idle']]
        labels = ['Successful', 'Collisions', 'Idle']
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        explode = (0.1, 0, 0)
        ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        ax2.set_title('Slot Status Distribution', fontsize=14, fontweight='bold')
        st.pyplot(fig2)

    with chart_col2:
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        display_slots = min(100, num_slots)
        slot_numbers = [s[0] for s in slots_data[:display_slots]]
        num_transmissions = [s[1] for s in slots_data[:display_slots]]
        statuses = [s[2] for s in slots_data[:display_slots]]
        colors_map = {'Idle': '#95a5a6', 'Success': '#2ecc71', 'Collision': '#e74c3c'}
        bar_colors = [colors_map[status] for status in statuses]
        ax3.bar(slot_numbers, num_transmissions, color=bar_colors, alpha=0.7)
        ax3.set_xlabel('Time Slot', fontsize=12)
        ax3.set_ylabel('Number of Transmissions', fontsize=12)
        ax3.set_title(f'Transmission Activity (First {display_slots} slots)', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ecc71', alpha=0.7, label='Success'),
            Patch(facecolor='#e74c3c', alpha=0.7, label='Collision'),
            Patch(facecolor='#95a5a6', alpha=0.7, label='Idle')
        ]
        ax3.legend(handles=legend_elements)
        st.pyplot(fig3)

    # 🔽 Save session data for Download.py
    st.session_state["aloha_results"] = {
        "num_nodes": num_nodes,
        "transmission_prob": transmission_prob,
        "num_slots": num_slots,
        "throughput": stats["throughput"],
        "efficiency": stats["efficiency"],
        "collisions": stats["collisions"],
        "idle": stats["idle"],
        "successful": stats["successful"],
        "offered_load": stats["offered_load"],
        "event_log": df_events
    }

    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    st.session_state["aloha_plot"] = buf

else:
    st.info("Set your parameters in the sidebar and click Run Simulation to start!")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 0.9rem; color: #666;">
        Developed for Computer Networks Project | Slotted ALOHA Protocol Simulator<br>
    </p>
</div>
""", unsafe_allow_html=True)
