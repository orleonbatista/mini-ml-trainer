import pandas as pd
from .default_datasets import load_iris_dataset
from .local_datasets import load_local_csv, load_local_excel

class DatasetManager:
    def __init__(self, default_dataset="iris"):
        self.default_dataset = default_dataset

    def load_default_dataset(self):
        """
        Carrega o dataset padrão definido em self.default_dataset.
        Atualmente suporta apenas 'iris'.
        """
        if self.default_dataset == "iris":
            return load_iris_dataset()
        else:
            raise ValueError(f"Dataset default '{self.default_dataset}' não suportado.")

    def load_local_dataset(self, file, file_type="csv"):
        """
        Carrega um dataset local a partir de um arquivo (objeto file).
        Suporta arquivos CSV ou Excel.
        """
        if file_type == "csv":
            return pd.read_csv(file)
        elif file_type in ["xls", "xlsx"]:
            return pd.read_excel(file)
        else:
            raise ValueError(f"Tipo de arquivo '{file_type}' não suportado.")
