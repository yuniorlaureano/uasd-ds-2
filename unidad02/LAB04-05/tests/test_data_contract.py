import pandas as pd
import pytest

from lab04_05.data import Data

def test_accepts_valid_dataframe():
    data = Data()
    df = pd.DataFrame({"text": ["uno", "dos"], "label": ["a", "b"]})
    data.validate_dataframe(df, "text", "label")


def test_rejects_missing_target():
    data = Data()
    df = pd.DataFrame({"text": ["uno"]})
    with pytest.raises(ValueError, match="Faltan columnas"):
        data.validate_dataframe(df, "text", "label")


def test_rejects_empty_text():
    data = Data()
    df = pd.DataFrame({"text": [""], "label": ["a"]})
    with pytest.raises(ValueError, match="Existen textos vacios"):
        data.validate_dataframe(df, "text", "label")