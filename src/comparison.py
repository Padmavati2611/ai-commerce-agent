import pandas as pd


def find_product(products, product_name):
    """
    Find a product using its product name.
    """

    if "product_name" not in products.columns:
        return None

    if not product_name:
        return None

    product_name = str(product_name).strip().lower()

    matches = products[
        products["product_name"]
        .astype(str)
        .str.strip()
        .str.lower()
        == product_name
    ]

    if matches.empty:
        return None

    return matches.iloc[0]


def compare_products(
    products,
    product_name_1,
    product_name_2
):
    """
    Find two products for comparison.
    """

    product_1 = find_product(
        products,
        product_name_1
    )

    product_2 = find_product(
        products,
        product_name_2
    )

    return product_1, product_2


def create_comparison_table(
    product_1,
    product_2
):
    """
    Create a comparison table.
    """

    if product_1 is None or product_2 is None:
        return pd.DataFrame()

    comparison = {
        "Product": [
            product_1.get(
                "product_name",
                "Product 1"
            ),
            product_2.get(
                "product_name",
                "Product 2"
            )
        ],

        "Brand": [
            product_1.get(
                "brand",
                "N/A"
            ),
            product_2.get(
                "brand",
                "N/A"
            )
        ],

        "Category": [
            product_1.get(
                "category",
                "N/A"
            ),
            product_2.get(
                "category",
                "N/A"
            )
        ],

        "Price": [
            product_1.get(
                "price",
                "N/A"
            ),
            product_2.get(
                "price",
                "N/A"
            )
        ],

        "Rating": [
            product_1.get(
                "rating_avg",
                "N/A"
            ),
            product_2.get(
                "rating_avg",
                "N/A"
            )
        ],

        "Reviews": [
            product_1.get(
                "review_count",
                "N/A"
            ),
            product_2.get(
                "review_count",
                "N/A"
            )
        ],

        "Stock": [
            product_1.get(
                "stock_quantity",
                "N/A"
            ),
            product_2.get(
                "stock_quantity",
                "N/A"
            )
        ]
    }

    return pd.DataFrame(comparison)


def compare_summary(
    product_1,
    product_2
):
    """
    Generate a simple comparison summary.
    """

    if product_1 is None or product_2 is None:
        return "Unable to compare the products."

    name_1 = product_1.get(
        "product_name",
        "Product 1"
    )

    name_2 = product_2.get(
        "product_name",
        "Product 2"
    )

    price_1 = pd.to_numeric(
        product_1.get("price"),
        errors="coerce"
    )

    price_2 = pd.to_numeric(
        product_2.get("price"),
        errors="coerce"
    )

    rating_1 = pd.to_numeric(
        product_1.get("rating_avg"),
        errors="coerce"
    )

    rating_2 = pd.to_numeric(
        product_2.get("rating_avg"),
        errors="coerce"
    )

    reviews_1 = pd.to_numeric(
        product_1.get("review_count"),
        errors="coerce"
    )

    reviews_2 = pd.to_numeric(
        product_2.get("review_count"),
        errors="coerce"
    )

    summary = []

    if pd.notna(price_1) and pd.notna(price_2):

        if price_1 < price_2:
            summary.append(
                f"💰 {name_1} is cheaper."
            )

        elif price_2 < price_1:
            summary.append(
                f"💰 {name_2} is cheaper."
            )

        else:
            summary.append(
                "💰 Both products have the same price."
            )

    if pd.notna(rating_1) and pd.notna(rating_2):

        if rating_1 > rating_2:
            summary.append(
                f"⭐ {name_1} has the higher rating."
            )

        elif rating_2 > rating_1:
            summary.append(
                f"⭐ {name_2} has the higher rating."
            )

        else:
            summary.append(
                "⭐ Both products have the same rating."
            )

    if pd.notna(reviews_1) and pd.notna(reviews_2):

        if reviews_1 > reviews_2:
            summary.append(
                f"💬 {name_1} has more reviews."
            )

        elif reviews_2 > reviews_1:
            summary.append(
                f"💬 {name_2} has more reviews."
            )

        else:
            summary.append(
                "💬 Both products have the same number of reviews."
            )

    if not summary:
        return (
            "There is not enough information "
            "to compare these products."
        )

    return "\n\n".join(summary)