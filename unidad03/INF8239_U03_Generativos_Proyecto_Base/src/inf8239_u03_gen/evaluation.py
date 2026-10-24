from __future__ import annotations

import numpy as np


def nearest_neighbors(queries: np.ndarray, references: np.ndarray, batch_size: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    """Índice y distancia euclidiana (por píxel, RMS) del vecino más cercano de cada consulta."""
    queries = queries.reshape(len(queries), -1).astype("float32")
    references = references.reshape(len(references), -1).astype("float32")
    best_index = np.zeros(len(queries), dtype=int)
    best_distance = np.full(len(queries), np.inf, dtype="float32")
    query_norms = (queries**2).sum(axis=1)[:, None]
    for start in range(0, len(references), batch_size):
        block = references[start : start + batch_size]
        squared = np.maximum(query_norms - 2 * queries @ block.T + (block**2).sum(axis=1)[None, :], 0)
        index = squared.argmin(axis=1)
        distance = squared[np.arange(len(queries)), index]
        improved = distance < best_distance
        best_index[improved] = index[improved] + start
        best_distance[improved] = distance[improved]
    return best_index, np.sqrt(best_distance / queries.shape[1])


def mean_pairwise_distance(images: np.ndarray) -> float:
    """Distancia RMS media entre todos los pares; valores bajos indican poca diversidad."""
    flat = images.reshape(len(images), -1).astype("float32")
    squared = np.maximum((flat**2).sum(1)[:, None] - 2 * flat @ flat.T + (flat**2).sum(1)[None, :], 0)
    upper = np.triu_indices(len(flat), k=1)
    return float(np.sqrt(squared[upper] / flat.shape[1]).mean())
