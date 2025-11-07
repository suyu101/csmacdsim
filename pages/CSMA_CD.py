import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import io

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="CSMA & CSMA/CD Simulator",
    page_icon="💻",
    layout="wide"
)
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
st.title("CSMA & CSMA/CD Protocol Simulator")
st.markdown("""
This simulator models Carrier Sense Multiple Access (CSMA) and CSMA/CD,
showing node-level timelines, collisions, backoff, and performance comparison.
""")
st.divider()

# --------------------- SIDEBAR ---------------------
st.sidebar.header("Simulation Parameters")

num_nodes = st.sidebar.slider("Number of Nodes", 2, 30, 6)
num_packets = st.sidebar.slider("Packets per Node", 1, 20, 5)
prop_delay = st.sidebar.number_input("Propagation Delay (slots)", 0.0, 5.0, 0.0, 0.1)
tx_time = st.sidebar.number_input("Packet Transmission Time (slots)", 1.0, 10.0, 1.0, 0.5)
packet_gen_prob = st.sidebar.slider("Probability of New Packet Generation", 0.0, 1.0, 0.12, 0.01)
protocol_type = st.sidebar.selectbox(
    "Protocol Type",
    ["1-Persistent CSMA", "Non-Persistent CSMA", "p-Persistent CSMA (CSMA/CD)"]
)
compare_protocols = st.sidebar.checkbox("Compare All Protocols (Efficiency & Throughput)")
compare_runs = st.sidebar.slider("Comparison: runs per protocol (avg)", 3, 20, 6)
run_simulation = st.sidebar.button("Run Simulation", type="primary")

# --------------------- SIMULATOR ---------------------
def simulate_csma(num_nodes, num_packets, prop_delay, tx_time, gen_prob, protocol, seed=None, max_time=400):
    if seed is not None:
        np.random.seed(seed)

    success_count = 0
    collision_count = 0
    usage_log = []
    node_timelines = {i: [] for i in range(num_nodes)}
    channel_busy_until = 0.0
    backoff = np.zeros(num_nodes)
    packet_ready = np.zeros(num_nodes)
    retransmission_attempts = np.zeros(num_nodes)

    for t in range(int(max_time)):
        for i in range(num_nodes):
            if np.random.rand() < gen_prob:
                packet_ready[i] = 1

        sensing_nodes = [i for i in range(num_nodes) if packet_ready[i] == 1 and backoff[i] <= 0]

        if t < channel_busy_until:
            if protocol == "Non-Persistent CSMA":
                for i in sensing_nodes:
                    backoff[i] = np.random.randint(2, 8)
            elif protocol == "p-Persistent CSMA (CSMA/CD)":
                p = 0.4
                sensing_nodes = [i for i in sensing_nodes if np.random.rand() < p]
            usage_log.append(("Busy", t))
            for n in range(num_nodes):
                node_timelines[n].append((t, 0))
            backoff = np.maximum(backoff - 1, 0)
            continue

        if len(sensing_nodes) == 0:
            usage_log.append(("Idle", t))
            for n in range(num_nodes):
                node_timelines[n].append((t, 0))
        elif len(sensing_nodes) == 1:
            node = sensing_nodes[0]
            success_count += 1
            usage_log.append((f"Success (Node {node})", t))
            packet_ready[node] = 0
            retransmission_attempts[node] = 0
            for n in range(num_nodes):
                node_timelines[n].append((t, 1 if n == node else 0))
            channel_busy_until = t + max(1.0, tx_time)
        else:
            collision_count += 1
            usage_log.append(("Collision", t))
            for i in sensing_nodes:
                retransmission_attempts[i] += 1
                k = int(min(retransmission_attempts[i], 10))
                backoff[i] = np.random.randint(1, 2 ** k)
            for n in range(num_nodes):
                node_timelines[n].append((t, 2 if n in sensing_nodes else 0))
            channel_busy_until = t + max(1.0, tx_time * 0.5)
        backoff = np.maximum(backoff - 1, 0)

    total_slots = int(max_time)
    efficiency = success_count / total_slots
    throughput = success_count / total_slots
    busy_slots = sum(1 for e, _ in usage_log if e != "Idle")
    utilization = busy_slots / total_slots
    return usage_log, success_count, collision_count, efficiency, throughput, utilization, node_timelines

# --------------------- PLOT ---------------------
def plot_node_gantt(node_timelines, max_time):
    colors = {0: '#d3d3d3', 1: '#32CD32', 2: '#FF6347'}
    labels = {0: 'Idle', 1: 'Successful Transmission', 2: 'Collision'}
    fig, ax = plt.subplots(figsize=(12, 0.6 * len(node_timelines) + 1))
    max_t = 0
    for i, (node, timeline) in enumerate(sorted(node_timelines.items())):
        for t, state in timeline:
            ax.barh(i, 1, left=t, color=colors[state], height=0.6)
            if t > max_t:
                max_t = t
    ax.set_xlabel("Time Slot")
    ax.set_ylabel("Node")
    ax.set_title("Node-level Activity Timeline (Gantt view)", fontsize=13, pad=8)
    ax.set_xlim(0, max(max_time, max_t + 1))
    ax.set_yticks(range(len(node_timelines)))
    ax.set_yticklabels([f"Node {n}" for n in sorted(node_timelines.keys())])
    ax.grid(axis='x', alpha=0.25)
    legend_patches = [Patch(color=colors[k], label=labels[k]) for k in sorted(labels.keys())]
    ax.legend(handles=legend_patches, loc='upper right', frameon=True)
    st.pyplot(fig)
    return fig

# --------------------- MAIN EXECUTION ---------------------
if run_simulation:
    seed0 = np.random.randint(0, 2**31 - 1)
    usage, success, collisions, efficiency, throughput, utilization, node_timeline = simulate_csma(
        num_nodes, num_packets, prop_delay, tx_time, packet_gen_prob, protocol_type, seed=seed0, max_time=400
    )

    st.subheader("Simulation Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Successful Transmissions", success)
    c2.metric("Collisions", collisions)
    c3.metric("Efficiency", f"{efficiency*100:.2f}%")
    c4.metric("Throughput", f"{throughput:.4f}")

    st.subheader("Channel Activity Timeline")
    fig = plot_node_gantt(node_timeline, max_time=400)

    st.subheader("Event Table")
    df = pd.DataFrame(usage, columns=["Event", "Time Slot"])
    st.dataframe(df, use_container_width=True)

    # Save results for Download.py
    st.session_state["csma_results"] = {
        "num_nodes": num_nodes,
        "num_packets": num_packets,
        "prop_delay": prop_delay,
        "tx_time": tx_time,
        "packet_gen_prob": packet_gen_prob,
        "protocol_type": protocol_type,
        "efficiency": efficiency,
        "throughput": throughput,
        "collisions": collisions,
        "success": success,
        "utilization": utilization,
        "event_log": df
    }

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.session_state["csma_plot"] = buf

else:
    st.info("Adjust parameters in the sidebar and click Run Simulation to start.")
