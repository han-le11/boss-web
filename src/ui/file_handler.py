

def find_bounds(df) -> bool:
    """
    Returns True if there are bounds in the uploaded file; otherwise False.
    :param df: data from the uploaded file that is read into a dataframe.
    :return:
    """
    bounds_exist = False
    if df is not None:
        x = df.filter(regex='boss-bound').dropna().to_numpy()
        if x.size != 0:
            # get a list of bound names
            bound_names = [k for k in list(df.columns) if 'boss-bound' in k]
            if len(bound_names) != 0:
                bounds_exist = True
    return bounds_exist




