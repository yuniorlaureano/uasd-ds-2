from ucimlrepo import fetch_ucirepo
from lab02.model import BanknoteAuhentication
import pandas as pd
from pathlib import Path
import os

class EmptyDatasetError(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

def fetch_bank_note_data() -> BanknoteAuhentication:
    response = fetch_ucirepo(id=267)
    banknote_authentication = BanknoteAuhentication(
        response.data.features,
        response.data.targets,
        response.metadata,
        response.variables
    )

    return banknote_authentication

def get_data_folder():
    path = Path(__file__)
    data_folder = os.path.join(path.resolve().parent.parent.parent, "data")
    print(path.resolve().parent.parent.parent)
    return data_folder

def fetch_bank_note_data_from_file() -> pd.DataFrame:
    data_folder = get_data_folder()
    banknote_file_path = os.path.join(data_folder, "data_banknote_authentication.txt")
    columns = ['variance', 'skewness', 'curtosis', 'entropy', 'target']
    banknote_df = pd.read_csv(banknote_file_path, header=None, names=columns)

    if banknote_df.empty:
        raise EmptyDatasetError()

    return banknote_df

if __name__ == "__main__":
    print(fetch_bank_note_data_from_file())