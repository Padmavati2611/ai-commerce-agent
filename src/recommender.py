import pandas as pd


def find_price_column(products):
    """
    Find the price column in the dataset.
    """

    if "price" in products.columns:
        return "price"

    return None


def filter_by_price(products, max_price):
    """
    Return products within the customer's budget.
    """

    price_column = find_price_column(products)

    if price_column is None:
        return pd.DataFrame()

    products = products.copy()

    products[price_column] = pd.to_numeric(
        products[price_column],
        errors="coerce"
    )

    products = products.dropna(
        subset=[price_column]
    )

    if max_price is None:
        return products

    results = products[
        products[price_column] <= max_price
    ]

    return results


def recommend_products(
    products,
    max_price=None,
    top_n=5
):
    """
    Recommend products using:
    - Rating
    - Review count
    - Price
    - Stock availability
    """

    products = products.copy()

    required_columns = [
        "price",
        "rating_avg",
        "review_count",
        "stock_quantity"
    ]

    for column in required_columns:

        if column not in products.columns:
            return products.head(top_n)

    products["price"] = pd.to_numeric(
        products["price"],
        errors="coerce"
    )

    products["rating_avg"] = pd.to_numeric(
        products["rating_avg"],
        errors="coerce"
    )

    products["review_count"] = pd.to_numeric(
        products["review_count"],
        errors="coerce"
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce"
    )

    products = products.dropna(
        subset=[
            "price",
            "rating_avg",
            "review_count",
            "stock_quantity"
        ]
    )

    if max_price is not None:

        products = products[
            products["price"] <= max_price
        ]

    if products.empty:
        return products

    # Prefer products that are in stock.
    products["stock_score"] = (
        products["stock_quantity"] > 0
    ).astype(int)

    # Limit review influence so very large
    # review counts do not dominate the score.
    review_score = (
        products["review_count"]
        .clip(upper=1000)
        / 100
    )

    # Lower prices receive a small advantage.
    price_score = (
        products["price"] / 100000
    )

    # Recommendation score.
    products["recommendation_score"] = (
        products["rating_avg"] * 10
        + review_score
        + products["stock_score"] * 2
        - price_score
    )

    products = products.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return products.head(top_n)