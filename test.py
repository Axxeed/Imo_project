import pytest
import pandas as pd
import numpy as np
from utils import alldrop

@pytest.fixture
def sample_data():
    """Creates a sample DataFrame for testing."""

    data = {
        "Code service sages": ["A123", "A123", "B456", None],
        "Reference document": ["DOC1", "DOC1", "DOC2", None],
        "Surface Carrez du 1er lot": [10.0, None, 15.0, 20.0],
        "1 Articles CGI": ["A123", "A123", "B456", None],
        "2 Articles CGI": ["DOC1", "DOC1", "DOC2", None],
        "3 Articles CGI": [10.0, None, 15.0, 20.0],
        "4 Articles CGI": ["DOC1", "DOC1", "DOC2", None],
        "5 Articles CGI": [10.0, None, 15.0, 20.0],
        "Section": ["DOC1", "DOC1", "DOC2", None],
        "No disposition": [10.0, None, 15.0, 20.0],
        "Nature culture": ["DOC1", "DOC1", "DOC2", None],
        "Nature culture speciale": [10.0, None, 15.0, 20.0],
        "Identifiant local": ["A123", "A123", "B456", None],
        "Prefixe de section": ["DOC1", "DOC1", "DOC2", None],
        "Surface Carrez du 2eme lot": [10.0, None, 15.0, 20.0],
        "2eme lot": ["DOC1", "DOC1", "DOC2", None],
        "3eme lot": [10.0, None, 15.0, 20.0],
        "4eme lot": ["DOC1", "DOC1", "DOC2", None],
        "5eme lot": [10.0, None, 15.0, 20.0],
        "No Volume": ["DOC1", "DOC1", "DOC2", None],
        "1er lot": [10.0, None, 15.0, 20.0],
        "No plan": ["A123", "A123", "B456", None],
        "Surface terrain": ["DOC1", "DOC1", "DOC2", None],
        "Surface reelle bati": [10.0, None, 15.0, 20.0],
        "Nombre de lots": ["DOC1", "DOC1", "DOC2", None],
        "B/T/Q": [10.0, None, 15.0, 20.0],
        "Surface Carrez du 3eme lot": ["DOC1", "DOC1", "DOC2", None],
        "Surface Carrez du 4eme lot": [10.0, None, 15.0, 20.0],
        "Surface Carrez du 5eme lot": ["DOC1", "DOC1", "DOC2", None],
        "Code type local": [10.0, None, 15.0, 20.0],
        "Nature mutation": [10.0, None, 15.0, 20.0],
    }
    return pd.DataFrame(data)


def test_alldrop_drops_duplicates(sample_data):
    """Tests if alldrop removes duplicate rows."""

    df_with_duplicates = pd.concat([sample_data] * 2)
    df_dropped = alldrop(df_with_duplicates.copy())

    assert df_dropped.shape[0] == 3  # Assert number of rows reduced


def test_alldrop_handles_nan_in_specified_column(sample_data):
    """Tests if alldrop removes rows with NaN in 'Surface Carrez du 1er lot'."""

    sample_data.loc[1, "Surface Carrez du 1er lot"] = np.nan
    df_dropped = alldrop(sample_data.copy())

    assert df_dropped.shape[0] == 3  # Assert one row removed due to NaN


def test_alldrop_removes_specified_columns(sample_data):
    """Tests if alldrop removes the specified columns."""

    expected_columns = list(sample_data.columns)
    for col in alldrop(sample_data.copy()).columns:
        expected_columns.remove(col)

    assert expected_columns != [
        "Surface Carrez du 1er lot",
        "Date mutation",
        "Valeur fonciere",
        "No voie",
        "Type de voie",
        "Code voie",
        "Voie",
        "Code postal",
        "Commune",
        "Code departement",
        "Code commune",
        "Surface Carrez du 1er lot",
        "Type local",
        "Nombre pieces principales",
        "id_vente"
    ]


if __name__ == "__main__":
    pytest.main()
