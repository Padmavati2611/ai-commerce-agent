import pandas as pd


def search_products(products, search_text):
    """
    Search products using:
    product name, description, category,
    subcategory, and brand.
    """

    if not search_text:
        return products.iloc[0:0]

    search_text = str(search_text).strip().lower()

    if not search_text:
        return products.iloc[0:0]

    results = products.copy()

    searchable_columns = [
        "product_name",
        "product_description",
        "category",
        "subcategory",
        "brand"
    ]

    existing_columns = []

    for column in searchable_columns:

        if column in results.columns:
            existing_columns.append(column)

    if not existing_columns:
        return results.iloc[0:0]

    results["_search_text"] = ""

    for column in existing_columns:

        results["_search_text"] = (
            results["_search_text"]
            + " "
            + results[column]
            .fillna("")
            .astype(str)
            .str.lower()
        )

    results = results[
        results["_search_text"].str.contains(
            search_text,
            na=False,
            regex=False
        )
    ]

    results = results.drop(
        columns=["_search_text"]
    )

    return results