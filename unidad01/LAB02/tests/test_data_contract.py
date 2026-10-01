from lab02.data import fetch_bank_note_data_from_file
import pytest
import pandas as pd

@pytest.fixture(scope="session")
def share_data() -> pd.DataFrame:
    data = fetch_bank_note_data_from_file()
    return data

def test_dataset_is_not_empty(share_data):
    assert not share_data.empty

def test_dataset_has_required_columns(share_data):
    columns = set(['variance', 'skewness', 'curtosis', 'entropy', 'target'])
    assert set(share_data.columns) == columns

def test_dataset_has_two_classes(share_data):
    y = share_data["target"]
    print(y.nunique())
    assert y.nunique() >= 2
