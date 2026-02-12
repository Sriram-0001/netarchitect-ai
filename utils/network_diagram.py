import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

import matplotlib.pyplot as plt

def plot_cost_breakdown(breakdown):

    labels = []
    values = []

    for item in breakdown.values():
        labels.append(item["model"])
        values.append(item["total"])

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    return fig
    if vendor_choice == "Cisco":
        st.pyplot(plot_cost_breakdown(result["cost"]["cisco_breakdown"]))


def generate_network_diagram(infra_package):

    design = infra_package["infrastructure_design"]
    components = design["components"]

    G = nx.Graph()

    G.add_node("Router")

    for i in range(components["switches"]):
        switch = f"Switch_{i+1}"
        G.add_node(switch)
        G.add_edge("Router", switch)

        for j in range(components["access_points"]):
            ap = f"AP_{i+1}_{j+1}"
            G.add_node(ap)
            G.add_edge(switch, ap)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1500)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return buffer
