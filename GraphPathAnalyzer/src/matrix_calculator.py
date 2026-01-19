import numpy as np


def is_valid_adjacency_matrix(matrix):
    """
    Verifica que la matriz sea cuadrada y contenga solo enteros no negativos.
    Esto es esencial porque una matriz de adyacencia representa conexiones entre nodos.
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        return False
    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
        for val in row:
            if not isinstance(val, int) or val < 0:
                return False
    return True


def calculate_power(matrix, m):
    """
    Calcula A^m usando multiplicación matricial entera.
    Cada elemento (i,j) en A^m indica el número de caminos de longitud m del nodo i al nodo j.
    """
    if m < 1:
        raise ValueError("La potencia m debe ser un entero ≥ 1.")
    A = np.array(matrix, dtype=int)
    result = np.linalg.matrix_power(A, m)
    return result.tolist()
