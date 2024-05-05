from speak_to_data.application.query_parser import QueryData


def generate_model_ready_dataset(dataset: list[dict],
                                 query_data: QueryData) -> list[dict[str, str]]:
    crop = query_data.crop
    action = query_data.action
    start_date, end_date = query_data.query_dates.date_range

    filter_rows = [
        row for row in dataset
        if row["crop"] in crop
        and row["action"] in action
        and start_date <= row["date"] <= end_date
    ]

    if not filter_rows:
        return filter_rows

    filter_columns = [
        {key: row[key] for key in row.keys() if key in query_data.columns}
        for row in filter_rows
    ]

    # Now the data needs to be transformed from a list of dicts representing rows
    # to a single dict with column names as keys and column values as values

    return filter_columns

def _list_of_dicts_to_one_dict(dataset: list[dict]) -> dict:
    """Transform list[dict[str, str]] into dict[str, list[str]]"""
    if not dataset:
        return dict()

    # Create dict_keys and dict_values objects
    key_view = dataset[0].keys()
    # dict.values() is cast as list to enable indexing in the dict comprehension
    value_views = tuple(list(row.values()) for row in dataset)
    # Construct a dict by enumerating the keys and selecting the matching value
    # from each member of value_views
    one_dict = {key: [value[idx] for value in value_views]
                for idx, key in enumerate(key_view)}
    return one_dict