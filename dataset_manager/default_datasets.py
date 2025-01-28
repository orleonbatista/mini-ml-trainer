from sklearn.datasets import load_iris
import pandas as pd

def load_iris_dataset():
    """
    Carrega e retorna o dataset Iris como um DataFrame do pandas.
    """
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df["target"] = iris.target
    return df
