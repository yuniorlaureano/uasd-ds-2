import numpy as np
import pytest

tf = pytest.importorskip("tensorflow")
from lab07.data import CLASS_NAMES
from lab07.models import build_cnn, build_dense


@pytest.mark.parametrize("factory", [build_cnn, build_dense])
def test_output_contract(factory):
    model = factory(tf)
    batch = np.random.default_rng(0).random((4, 28, 28, 1), dtype="float32")
    probabilities = model(batch).numpy()
    assert probabilities.shape == (4, len(CLASS_NAMES))
    assert np.isfinite(probabilities).all()
    assert (probabilities >= 0).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-5)
