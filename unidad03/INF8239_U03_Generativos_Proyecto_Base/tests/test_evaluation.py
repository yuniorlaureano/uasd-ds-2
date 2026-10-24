import numpy as np

from inf8239_u03_gen.evaluation import mean_pairwise_distance, nearest_neighbors


def test_nearest_neighbor_finds_exact_copy_across_batches():
    rng = np.random.default_rng(0)
    references = rng.random((50, 28, 28, 1), dtype=np.float32)
    index, distance = nearest_neighbors(references[[7, 42]], references, batch_size=16)
    assert index.tolist() == [7, 42]
    assert np.allclose(distance, 0, atol=1e-3)


def test_identical_samples_have_zero_diversity():
    assert mean_pairwise_distance(np.ones((4, 28, 28, 1))) == 0
    assert mean_pairwise_distance(np.eye(4)) > 0
