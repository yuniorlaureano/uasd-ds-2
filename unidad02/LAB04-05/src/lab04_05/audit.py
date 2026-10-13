import pandas as pd

class Audit:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
    
    def get_columns(self):
        return list(self.dataset.columns)

    def get_shape(self):
        return self.dataset.shape

    def get_duplicate_count(self):
        return self.dataset.duplicated().sum()

    def get_distribution(self, column):
        return self.dataset[column].value_counts(dropna=False, normalize=True)

    def get_longitud_de_textos(self, column):
        return self.dataset[column].str.len().quantile([0, 0.25, 0.5, 0.75, 1]).head(100)

    def describe_dataset(self):
        df_detail = pd.DataFrame({
            "tipo": self.dataset.dtypes.astype(str),
            "ausentes": self.dataset.isna().sum()
        })
        return df_detail.head(100)

    def __str__(self):
        audit_details = ""
        audit_details += f'- columns: {self.get_columns()}\n'
        audit_details += f'- shape: {self.get_shape()}\n'
        audit_details += f'- shape: {self.get_duplicate_count()}\n'
        audit_details += f'- distribution: \n  {self.get_distribution("label")}\n'
        audit_details += f'-----------Summary------------------------\n'
        audit_details += f'{self.describe_dataset()}\n'
        audit_details += f'-----------ongitudes de textos------------\n'
        audit_details += f'{self.get_longitud_de_textos("text")}\n'
        audit_details += f'------------------------------------------\n'

        return audit_details

if __name__ == "__main__":
    df = pd.DataFrame({
        "text": ['hola', 'mundo', 'desde', 'python'],
        "label": [0, 1, 0, 1]
    })
    audit = Audit(df)
    print(audit)