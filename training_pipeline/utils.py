import json
from typing import Optional, List

def parse_model_params(model_params_str: str) -> dict:
    """
    Converte uma string JSON em dict de parâmetros do modelo.
    Exemplo: '{"n_estimators": 100, "max_depth": 5}'
    """
    try:
        return json.loads(model_params_str)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"Erro ao parsear model_params: {e}")

def parse_columns_to_drop(columns_to_drop_str: Optional[str]) -> Optional[List[str]]:
    """
    Converte uma string JSON em lista de colunas a serem removidas.
    Exemplo: '["col1", "col2"]' -> ["col1", "col2"]
    """
    if columns_to_drop_str:
        try:
            return json.loads(columns_to_drop_str)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Erro ao parsear columns_to_drop: {e}")
    return None