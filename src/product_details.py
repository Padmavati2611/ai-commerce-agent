import pandas as pd


def get_product_details(products, product_id):
    """
    Find and return a product using its product ID.
    """

    if "product_id" not in products.columns:
        return None

    if product_id is None:
        return None

    product_id = str(product_id).strip()

    matches = products[
        products["product_id"]
        .astype(str)
        .str.strip()
        == product_id
    ]

    if matches.empty:
        return None

    return matches.iloc[0]


def get_product_name(product):
    """
    Return the product name.
    """

    if product is None:
        return "Unknown Product"

    if "product_name" in product.index:
        return str(product["product_name"])

    return "Unknown Product"


def get_product_price(product):
    """
    Return the product price.
    """

    if product is None:
        return None

    if "price" not in product.index:
        return None

    try:
        return float(product["price"])
    except (ValueError, TypeError):
        return None


def get_product_rating(product):
    """
    Return the product rating.
    """

    if product is None:
        return None

    if "rating_avg" not in product.index:
        return None

    try:
        return float(product["rating_avg"])
    except (ValueError, TypeError):
        return None


def get_product_stock(product):
    """
    Return the available stock quantity.
    """

    if product is None:
        return None

    if "stock_quantity" not in product.index:
        return None

    try:
        return int(float(product["stock_quantity"]))
    except (ValueError, TypeError):
        return None


def get_product_summary(product):
    """
    Create a simple product summary.
    """

    if product is None:
        return "Product not found."

    name = get_product_name(product)

    price = get_product_price(product)

    rating = get_product_rating(product)

    stock = get_product_stock(product)

    summary = f"Product: {name}"

    if price is not None:
        summary += f"\nPrice: ₹{price}"

    if rating is not None:
        summary += f"\nRating: {rating}"

    if stock is not None:
        summary += f"\nStock: {stock}"

    if "brand" in product.index:
        summary += f"\nBrand: {product['brand']}"

    if "category" in product.index:
        summary += f"\nCategory: {product['category']}"

    if "product_description" in product.index:
        summary += (
            f"\nDescription: "
            f"{product['product_description']}"
        )

    return summary