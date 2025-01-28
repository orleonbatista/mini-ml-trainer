import os
import joblib
import pandas as pd

from typing import Optional, List
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.base import ClassifierMixin

class Trainer:
    def __init__(
        self,
        model_dir: str,
        model_class,
        model_params: dict = None
    ):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

        self.model_file = os.path.join(self.model_dir, "model.pkl")
        self.model_class = model_class
        self.model_params = model_params or {}
        self.model = None

        # Guarda LabelEncoders para colunas categóricas
        self.label_encoders = {}

    def _drop_columns(self, data: pd.DataFrame, columns_to_drop: Optional[List[str]]) -> pd.DataFrame:
        if columns_to_drop:
            for col in columns_to_drop:
                if col in data.columns:
                    data = data.drop(columns=[col])
        return data

    def _preprocess_train(
        self,
        data: pd.DataFrame,
        columns_to_drop: Optional[List[str]] = None
    ) -> pd.DataFrame:
        data = self._drop_columns(data, columns_to_drop)
        data = data.fillna(data.mean(numeric_only=True))

        for col in data.select_dtypes(include=["object"]).columns:
            data[col] = data[col].fillna(data[col].mode()[0])

        # Codificação das colunas categóricas
        for col in data.select_dtypes(include=["object"]).columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            self.label_encoders[col] = le

        return data

    def _preprocess_predict(
        self,
        data: pd.DataFrame,
        columns_to_drop: Optional[List[str]] = None
    ) -> pd.DataFrame:
        data = self._drop_columns(data, columns_to_drop)
        data = data.fillna(data.mean(numeric_only=True))

        for col in data.select_dtypes(include=["object"]).columns:
            data[col] = data[col].fillna(data[col].mode()[0])
            if col in self.label_encoders:
                data[col] = self.label_encoders[col].transform(data[col])
            else:
                raise ValueError(
                    f"A coluna categórica '{col}' não foi vista no treinamento (encoder ausente)."
                )

        return data

    def train(
        self,
        data: pd.DataFrame,
        target_column: Optional[str] = None,
        columns_to_drop: Optional[List[str]] = None
    ):
        data = self._preprocess_train(data, columns_to_drop=columns_to_drop)

        if target_column and target_column in data.columns:
            y = data[target_column]
            X = data.drop(columns=[target_column])
        else:
            X = data.iloc[:, :-1]
            y = data.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = self.model_class(**self.model_params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        if issubclass(self.model_class, ClassifierMixin):
            metric_value = accuracy_score(y_test, y_pred)
            metric_name = "accuracy"
        else:
            metric_value = r2_score(y_test, y_pred)
            metric_name = "r2_score"

        artifacts = {
            "model": model,
            "label_encoders": self.label_encoders
        }
        joblib.dump(artifacts, self.model_file)

        return {metric_name: metric_value}, self.model_file

    def predict(
        self,
        data: pd.DataFrame,
        columns_to_drop: Optional[List[str]] = None
    ):
        if not os.path.exists(self.model_file):
            raise FileNotFoundError("Modelo não encontrado. Treine o modelo antes de realizar previsões.")

        if self.model is None:
            artifacts = joblib.load(self.model_file)
            self.model = artifacts["model"]
            self.label_encoders = artifacts["label_encoders"]

        data = self._preprocess_predict(data, columns_to_drop=columns_to_drop)
        return self.model.predict(data).tolist()

    def load_model(self):
        if not os.path.exists(self.model_file):
            raise FileNotFoundError(f"Modelo não encontrado em {self.model_file}. Treine primeiro.")
        artifacts = joblib.load(self.model_file)
        self.model = artifacts["model"]
        self.label_encoders = artifacts["label_encoders"]