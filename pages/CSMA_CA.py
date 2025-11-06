#fill code

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="CSMA/CA Simulator",
    page_icon="📶",
    layout="wide"
)

st.sidebar.page_link('Home.py', label='Home')
#st.sidebar.page_link('pages/CSMA_CA.py', label='CSMA/CA')
st.sidebar.page_link('pages/CSMA_CD.py', label='CSMA/CD')
#st.sidebar.page_link('pages/Pure_Aloha.py', label='Pure Aloha')
st.sidebar.page_link('pages/Slotted_Aloha.py', label='Slotted Aloha')
st.sidebar.markdown("---")
st.divider()


# Navigation bar
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
st.title("CSMA/CA Protocol Simulator")

st.markdown("""
This simulator models **Carrier Sense Multiple Access with Collision Avoidance (CSMA/CA)**, 
demonstrating how nodes avoid collisions by using *backoff*, *RTS/CTS* handshakes, 
and *acknowledgment mechanisms*.
""")
st.divider()

# --------------------- SIDEBAR ---------------------
st.sidebar.header("Simulation Parameters")

num_nodes = st.sidebar.slider("Number of Nodes", 2, 30, 6)
num_packets = st.sidebar.slider("Packets per Node", 1, 20, 5)
prop_delay = st.sidebar.number_input("Propagation Delay (slots)", 0.0, 5.0, 0.0, 0.1)
tx_time = st.sidebar.number_input("Transmission Time (slots)", 1.0, 10.0, 1.0, 0.5)
packet_gen_prob = st.sidebar.slider("Packet Generation Probability", 0.0, 1.0, 0.1, 0.01)
protocol_type = st.sidebar.selectbox(
    "CSMA/CA Variant",
    ["Basic CSMA/CA", "CSMA/CA with RTS/CTS"]
)
compare_protocols = st.sidebar.checkbox("Compare Both Variants (avg)")
compare_runs = st.sidebar.slider("Comparison: runs per variant", 3, 20, 5)
run_simulation = st.sidebar.button("Run Simulation", type="primary")

# --------------------- SIMULATOR ---------------------
def simulate_csma_ca(num_nodes, num_packets, prop_delay, tx_time, gen_prob, variant="Basic CSMA/CA", seed=None, max_time=400):
    if seed is not None:
        np.random.seed(seed)

    success_count = 0
    collision_count = 0
    usage_log = []
    node_timelines = {i: [] for i in range(num_nodes)}

    channel_busy_until = 0.0
    backoff = np.zeros(num_nodes)
    packet_ready = np.zeros(num_nodes)
    waiting_ack = np.zeros(num_nodes)

    for t in range(int(max_time)):
        # Packet generation
        for i in range(num_nodes):
            if np.random.rand() < gen_prob:
                packet_ready[i] = 1

        active_nodes = [i for i in range(num_nodes) if packet_ready[i] == 1 and backoff[i] <= 0]

        # Channel busy
        if t < channel_busy_until:
            usage_log.append(("Busy", t))
            for n in range(num_nodes):
                node_timelines[n].append((t, 0))
            backoff = np.maximum(backoff - 1, 0)
            continue

        if len(active_nodes) == 0:
            usage_log.append(("Idle", t))
            for n in range(num_nodes):
                node_timelines[n].append((t, 0))
        elif len(active_nodes) == 1:
            node = active_nodes[0]
            success_count += 1
            usage_log.append((f"Success (Node {node})", t))

            # RTS/CTS handshake delay
            if variant == "CSMA/CA with RTS/CTS":
                handshake_time = 0.5 * tx_time
                channel_busy_until = t + tx_time + handshake_time
            else:
                channel_busy_until = t + tx_time

            packet_ready[node] = 0
            for n in range(num_nodes):
                node_timelines[n].append((t, 1 if n == node else 0))
        else:
            # Virtual collisions due to RTS overlaps
            collision_count += 1
            usage_log.append(("Collision", t))
            for i in active_nodes:
                backoff[i] = np.random.randint(1, 8)
            for n in range(num_nodes):
                node_timelines[n].append((t, 2 if n in active_nodes else 0))
            channel_busy_until = t + tx_time * 0.5

        backoff = np.maximum(backoff - 1, 0)

    total_slots = int(max_time)
    efficiency = success_count / total_slots if total_slots else 0
    throughput = success_count / total_slots if total_slots else 0
    busy_slots = sum(1 for e, _ in usage_log if e != "Idle")
    utilization = busy_slots / total_slots if total_slots else 0

    return usage_log, success_count, collision_count, efficiency, throughput, utilization, node_timelines

# --------------------- PLOT TIMELINE ---------------------
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

# --------------------- COMPARISON ---------------------
def run_compare(protocols, runs, **kwargs):
    effs, thrs, utils = [], [], []
    for proto in protocols:
        e_list, t_list, u_list = [], [], []
        for _ in range(runs):
            seed = np.random.randint(0, 2**31 - 1)
            _, _, _, eff, thr, util, _ = simulate_csma_ca(
                kwargs['num_nodes'], kwargs['num_packets'],
                kwargs['prop_delay'], kwargs['tx_time'],
                kwargs['gen_prob'], proto, seed=seed, max_time=kwargs.get('max_time', 400)
            )
            e_list.append(eff)
            t_list.append(thr)
            u_list.append(util)
        effs.append(np.mean(e_list))
        thrs.append(np.mean(t_list))
        utils.append(np.mean(u_list))
    return effs, thrs, utils

# --------------------- MAIN EXECUTION ---------------------
if run_simulation:
    st.spinner("Running simulation...")

    seed0 = np.random.randint(0, 2**31 - 1)
    usage, success, collisions, eff, thr, util, timelines = simulate_csma_ca(
        num_nodes, num_packets, prop_delay, tx_time, packet_gen_prob, variant=protocol_type, seed=seed0, max_time=400
    )

    st.subheader("Simulation Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Successful Transmissions", success)
    c2.metric("Collisions", collisions)
    c3.metric("Efficiency", f"{eff*100:.2f}%")
    c4.metric("Throughput (pkts/slot)", f"{thr:.4f}")

    st.divider()

    st.subheader("Node Timeline")
    plot_node_gantt(timelines, max_time=400)

    df = pd.DataFrame(usage, columns=["Event", "Time Slot"])
    st.dataframe(df, use_container_width=True)
    st.download_button("Download Event Data (CSV)", df.to_csv(index=False), "csma_ca_events.csv", "text/csv")

    if compare_protocols:
        st.subheader("Comparison of CSMA/CA Variants (avg)")
        protocols = ["Basic CSMA/CA", "CSMA/CA with RTS/CTS"]
        effs, thrs, utils = run_compare(
            protocols, compare_runs,
            num_nodes=num_nodes, num_packets=num_packets,
            prop_delay=prop_delay, tx_time=tx_time,
            gen_prob=packet_gen_prob, max_time=400
        )

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        labels = ["Efficiency (%)", "Throughput (pkts/slot)", "Utilization (%)"]
        data = [[e * 100 for e in effs], thrs, [u * 100 for u in utils]]

        for i, ax in enumerate(axes):
            ax.bar(protocols, data[i])
            ax.set_title(labels[i])
            ax.set_xticklabels(protocols, rotation=15, ha='right', fontsize=9)
            for j, v in enumerate(data[i]):
                ax.text(j, v + (max(data[i]) * 0.02), f"{v:.2f}", ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

        comp_df = pd.DataFrame({
            "Protocol": protocols,
            "Avg Efficiency (%)": [round(e * 100, 2) for e in effs],
            "Avg Throughput (pkts/slot)": [round(t, 4) for t in thrs],
            "Avg Utilization (%)": [round(u * 100, 2) for u in utils]
        })
        st.download_button("Download Comparison (CSV)", comp_df.to_csv(index=False),
                           "csma_ca_comparison.csv", "text/csv")

else:
    st.info("Adjust the parameters in the sidebar and click **Run Simulation** to start.")
    st.markdown("""
    ### Notes
    - **Basic CSMA/CA**: Avoids collisions by waiting random backoff periods before transmitting.  
    - **CSMA/CA with RTS/CTS**: Uses short handshake frames to reserve the channel and reduce hidden-node collisions.  
    """)

st.divider()
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 0.9rem; color: #666;">
        Developed for Computer Networks Project | CSMA/CA Simulator
    </p>
</div>
""", unsafe_allow_html=True)
