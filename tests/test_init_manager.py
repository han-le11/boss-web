import numpy as np
from src.tabs.init_manager_tab import InitManagerTab


def test_add_var_names_create_dataframe():
    init = InitManagerTab()
    init.dim = 2
    init_arr = np.array([[1, 2], [3, 4], [5, 4], [6, 5]])
    names_and_bounds = {"x": (0, 1), "y": (0, 1), "z": None}
    expected_columns = ["x", "y", "z"]
    df = init.add_var_names(init_arr, names_and_bounds)
    assert df.columns.tolist() == expected_columns
    assert df.shape == (4, 3)
