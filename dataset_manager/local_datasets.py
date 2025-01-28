import pandas as pd

def load_local_csv(file_path):
    """
    Carrega um arquivo CSV a partir de um caminho local.
    """
    return pd.read_csv(file_path)

def load_local_excel(file_path):
    """
    Carrega um arquivo Excel a partir de um caminho local (xls ou xlsx).
    """
    return pd.read_excel(file_path)
