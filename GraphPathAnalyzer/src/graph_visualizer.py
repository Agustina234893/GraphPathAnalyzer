import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def create_graph_from_matrix(matrix):
    """
    Convierte una matriz de adyacencia en un grafo dirigido (DiGraph) de NetworkX.
    Los nodos se etiquetan desde 1 hasta n (1-indexados).
    Las aristas llevan el peso igual al valor en la matriz (número de conexiones).
    """
    G = nx.DiGraph()
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            weight = matrix[i][j]
            if weight > 0:
                G.add_edge(i + 1, j + 1, weight=weight)
    return G


def plot_graph_to_base64(G):
    """
    Genera una imagen del grafo y la devuelve como cadena en base64.
    Esto permite incrustarla directamente en una página web (como Streamlit).
    """
    plt.figure(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)  # Layout consistente
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=12,
        font_weight="bold",
        arrows=True,
        arrowsize=15,
    )
    # Mostrar los pesos en las aristas si son > 1
    labels = nx.get_edge_attributes(G, "weight")
    if any(w > 1 for w in labels.values()):
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()  # ¡Importante! Libera memoria
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return img_str
