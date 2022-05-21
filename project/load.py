"""Data adapters."""
import pandas as pd
from pandera.decorators import check_types
from pandera.typing import DataFrame

from project.schema import IrisData


@check_types
def load_iris_data() -> DataFrame[IrisData]:
    """Load and return iris data.

    Returns:
        DataFrame[IrisData]: iris data
    """
    file_name = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"
    iris_data = pd.read_csv(file_name)
    return iris_data
