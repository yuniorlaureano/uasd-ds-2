import numpy as np
import pytest

from lab07.data import CLASS_NAMES, normalize_images, validate_images


def test_normalize_adds_channel_and_scales():
    raw = np.array([[[0] * 28] * 28, [[255] * 28] * 28], dtype=np.uint8)
    result = normalize_images(raw)
    assert result.shape == (2, 28, 28, 1)
    assert result.min() == 0
    assert result.max() == 1


def test_validate_rejects_wrong_shape():
    with pytest.raises(ValueError, match="Forma inesperada"):
        validate_images(np.zeros((2, 28, 28)), np.zeros(2))


def test_validate_rejects_out_of_range():
    with pytest.raises(ValueError, match="normalizadas"):
        validate_images(np.full((2, 28, 28, 1), 255.0), np.zeros(2))


def test_validate_rejects_label_mismatch():
    with pytest.raises(ValueError, match="no coinciden"):
        validate_images(np.zeros((2, 28, 28, 1)), np.zeros(3))


def test_ten_classes():
    assert len(CLASS_NAMES) == 10
    assert len(set(CLASS_NAMES)) == 10
