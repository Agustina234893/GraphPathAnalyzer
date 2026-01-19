import streamlit as st
import pandas as pd
from src.matrix_calculator import is_valid_adjacency_matrix, calculate_power
from src.graph_visualizer import create_graph_from_matrix, plot_graph_to_base64

st.set_page_config(page_title="GraphPath Analyzer", layout="wide")
st.title(" GraphPath Analyzer")
st.markdown("Calcula caminos en grafos usando matrices de adyacencia.")

example_matrix = [
    [2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1],
    [0, 3, 2, 0, 3],
    [0, 2, 1, 0, 2],
    [4, 1, 2, 4, 1],
]

with st.expander("ℹ️ Instrucciones"):
    st.write(
        """
    - Ingresa una **matriz de adyacencia cuadrada** (solo enteros ≥ 0).
    - Elige una potencia **m ≥ 1**.
    - La app calculará **A^m**: cada celda (i,j) indica cuántos caminos hay de longitud **m** del nodo i al nodo j.
    """
    )

input_option = st.radio(
    "Elige cómo ingresar la matriz:", ("Manual", "Usar ejemplo del taller")
)

if input_option == "Manual":
    n = st.number_input(
        "Número de nodos (n):", min_value=2, max_value=10, value=3, step=1
    )
    user_matrix = []
    cols = st.columns(n)
    for i in range(n):
        row = []
        for j in range(n):
            val = cols[j].number_input(
                f"({i+1},{j+1})", min_value=0, value=0, key=f"{i}-{j}"
            )
            row.append(val)
        user_matrix.append(row)
else:
    user_matrix = example_matrix
    st.write("Matriz del taller cargada:")
    st.dataframe(pd.DataFrame(user_matrix))

m = st.number_input("Potencia m:", min_value=1, value=3, step=1, key="power_m")

if st.button(" Calcular A^m"):
    if not is_valid_adjacency_matrix(user_matrix):
        st.error(" Matriz inválida: debe ser cuadrada y contener solo enteros ≥ 0.")
    else:
        try:
            result = calculate_power(user_matrix, m)
            st.success(f" Resultado: A^{m}")
            df_result = pd.DataFrame(
                result,
                columns=[f"Nodo {j+1}" for j in range(len(result))],
                index=[f"Nodo {i+1}" for i in range(len(result))],
            )
            st.dataframe(df_result)

            G = create_graph_from_matrix(user_matrix)
            img_b64 = plot_graph_to_base64(G)
            st.markdown("### Grafo original:")
            st.markdown(
                f'<img src="image/png;base64,{img_b64}" width="500">',
                unsafe_allow_html=True,
            )

            st.markdown("### ¿Qué significa un valor?")
            i_sel = st.selectbox(
                "Fila (origen):",
                options=range(1, len(result) + 1),
                index=min(4, len(result) - 1),
            )
            j_sel = st.selectbox(
                "Columna (destino):",
                options=range(1, len(result) + 1),
                index=min(3, len(result) - 1),
            )
            val = result[i_sel - 1][j_sel - 1]
            st.info(
                f"Hay **{val} caminos** de longitud **{m}** desde el **Nodo {i_sel}** hasta el **Nodo {j_sel}**."
            )

        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
