import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="Slotted ALOHA Simulator", page_icon="📡", layout="wide")
st.sidebar.page_link('Home.py', label='Home')
st.sidebar.page_link('pages/CSMA_CD.py', label='CSMA/CD')
st.sidebar.page_link('pages/Slotted_Aloha.py', label='Slotted_Aloha')
st.sidebar.markdown("---")

st.divider()

# --------------------- NAVBAR ---------------------
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

# --------------------- TITLE ---------------------
st.title("Slotted ALOHA Protocol Simulator")
st.markdown("""
This simulator demonstrates the Slotted ALOHA protocol, a random access protocol 
where time is divided into slots and nodes can only transmit at the beginning of a slot.
""")

# --------------------- SIDEBAR ---------------------
st.sidebar.header("Simulation Parameters")
num_nodes = st.sidebar.slider("Number of Nodes", 2, 50, 10)
transmission_prob = st.sidebar.slider("Transmission Probability (p)", 0.01, 1.0, 0.3, 0.01)
num_slots = st.sidebar.slider("Number of Time Slots", 100, 5000, 1000, 100)
run_simulation = st.sidebar.button("Run Simulation", type="primary")

def simulate_slotted_aloha(num_nodes, p, num_slots):
    slots_data = []
    node_transmissions = {i: [] for i in range(num_nodes)}
    successful_transmissions, collisions, idle_slots = 0, 0, 0

    for slot in range(num_slots):
        transmitting_nodes = np.random.random(num_nodes) < p
        num_tx = np.sum(transmitting_nodes)
        tx_ids = [i for i in range(num_nodes) if transmitting_nodes[i]]

        if num_tx == 0:
            status = "Idle"; idle_slots += 1
            for i in range(num_nodes): node_transmissions[i].append((slot, 0))
        elif num_tx == 1:
            status = "Success"; successful_transmissions += 1
            for i in range(num_nodes): node_transmissions[i].append((slot, 1 if i in tx_ids else 0))
        else:
            status = "Collision"; collisions += 1
            for i in range(num_nodes): node_transmissions[i].append((slot, 2 if i in tx_ids else 0))
        slots_data.append((slot, num_tx, status))

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

def get_theoretical_throughput(G): return G * np.exp(-G)

def plot_timeline(node_transmissions, limit=50):
    colors = {0: '#d3d3d3', 1: '#2ecc71', 2: '#e74c3c'}
    fig, ax = plt.subplots(figsize=(12, 6))
    for node, trans in node_transmissions.items():
        for slot, state in trans[:limit]:
            ax.barh(node, 1, left=slot, color=colors[state], height=0.6)
    ax.set_xlabel("Time Slot"); ax.set_ylabel("Node")
    ax.set_title("Node Timeline (first 50 slots)")
    st.pyplot(fig)
    return fig

# --------------------- RUN SIMULATION ---------------------
if run_simulation:
    slots_data, node_transmissions, stats = simulate_slotted_aloha(num_nodes, transmission_prob, num_slots)

    st.header("Simulation Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Throughput (S)", f"{stats['throughput']:.4f}")
    col2.metric("Success Rate", f"{(stats['successful']/num_slots)*100:.1f}%")
    col3.metric("Collision Rate", f"{(stats['collisions']/num_slots)*100:.1f}%")
    col4.metric("Idle Rate", f"{(stats['idle']/num_slots)*100:.1f}%")

    st.subheader("Event Table")
    df = pd.DataFrame(slots_data, columns=["Slot", "Num Transmissions", "Status"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Throughput vs Offered Load")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    G = np.linspace(0, 5, 100)
    ax1.plot(G, get_theoretical_throughput(G), label="Theoretical")
    ax1.plot(stats["offered_load"], stats["throughput"], "ro", label="Simulated")
    ax1.set_xlabel("Offered Load (G)"); ax1.set_ylabel("Throughput (S)")
    ax1.legend(); ax1.grid(True)
    st.pyplot(fig1)

    # Save for Download.py
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
        "event_log": df
    }
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    st.session_state["aloha_plot"] = buf

else:
    st.info("Set parameters and click Run Simulation to start.")
