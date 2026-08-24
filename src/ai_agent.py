import re
import pandas as pd

from src.product_search import search_products

from src.recommender import (
    filter_by_price,
    recommend_products
)


# ============================================================
# EXTRACT BUDGET
# ============================================================

def extract_budget(text):
    """
    Find a budget amount from the customer's message.
    """

    numbers = re.findall(
        r"\d[\d,]*",
        text
    )

    if not numbers:

        return None

    budgets = []

    for number in numbers:

        number = number.replace(
            ",",
            ""
        )

        try:

            budgets.append(
                float(number)
            )

        except ValueError:

            pass

    if not budgets:

        return None

    return max(budgets)


# ============================================================
# EXTRACT PRODUCT KEYWORD
# ============================================================

def extract_product_keyword(text):
    """
    Find a useful product keyword.
    """

    query = text.lower()

    keywords = [

        "laptop",
        "phone",
        "smartphone",
        "mobile",
        "headphone",
        "headphones",
        "tablet",
        "watch",
        "camera",
        "television",
        "tv",
        "monitor",
        "keyboard",
        "mouse"

    ]

    for keyword in keywords:

        if keyword in query:

            return keyword

    return query


# ============================================================
# UNDERSTAND CUSTOMER QUERY
# ============================================================

def understand_query(user_query):
    """
    Understand the customer's basic intention.
    """

    query = user_query.lower()

    intent = "search"


    # Compare products

    if "compare" in query:

        intent = "compare"


    # Recommendation

    elif (
        "recommend" in query
        or "best" in query
        or "suggest" in query
    ):

        intent = "recommend"


    # Questions

    elif (
        "which" in query
        or "what" in query
        or "how" in query
        or "who" in query
    ):

        intent = "question"


    # Product details

    elif (
        "details" in query
        or "information" in query
        or "about" in query
    ):

        intent = "details"


    budget = extract_budget(
        query
    )

    product_keyword = extract_product_keyword(
        query
    )


    return {

        "intent": intent,

        "budget": budget,

        "keyword": product_keyword,

        "query": query

    }


# ============================================================
# RUN AGENT
# ============================================================

def run_agent(
    user_query,
    products
):
    """
    Process the customer's request
    and recommend suitable products.
    """

    result = understand_query(
        user_query
    )

    keyword = result["keyword"]

    budget = result["budget"]


    # --------------------------------
    # Search products
    # --------------------------------

    search_results = search_products(
        products,
        keyword
    )


    # --------------------------------
    # Apply budget
    # --------------------------------

    if budget is not None:

        search_results = filter_by_price(
            search_results,
            budget
        )


    # --------------------------------
    # Generate recommendations
    # --------------------------------

    recommendations = recommend_products(
        search_results,
        max_price=budget,
        top_n=5
    )


    return (
        result,
        recommendations
    )


# ============================================================
# ANSWER CUSTOMER QUESTIONS
# ============================================================

def answer_customer_question(
    user_query,
    products
):
    """
    Answer customer questions using
    the available product dataset.
    """

    result = understand_query(
        user_query
    )

    keyword = result["keyword"]

    query = result["query"]


    # --------------------------------
    # Search products
    # --------------------------------

    search_results = search_products(
        products,
        keyword
    )


    if search_results.empty:

        return (
            "I could not find products "
            f"matching '{keyword}'."
        )


    # ========================================================
    # BEST RATING
    # ========================================================

    if (
        "best rating" in query
        or "highest rating" in query
        or "best rated" in query
        or "highest rated" in query
    ):

        if "rating_avg" not in search_results.columns:

            return (
                "The dataset does not contain "
                "rating information."
            )


        search_results = search_results.copy()


        search_results["rating_avg"] = pd.to_numeric(
            search_results["rating_avg"],
            errors="coerce"
        )


        search_results = search_results.dropna(
            subset=["rating_avg"]
        )


        if search_results.empty:

            return (
                "I could not find products "
                "with valid ratings."
            )


        best_product = search_results.loc[
            search_results[
                "rating_avg"
            ].idxmax()
        ]


        product_name = best_product.get(
            "product_name",
            "the product"
        )


        rating = best_product[
            "rating_avg"
        ]


        return (
            f"The highest-rated {keyword} "
            f"is '{product_name}' "
            f"with a rating of {rating}."
        )


    # ========================================================
    # CHEAPEST PRODUCT
    # ========================================================

    if (
        "cheapest" in query
        or "lowest price" in query
        or "least expensive" in query
    ):

        if "price" not in search_results.columns:

            return (
                "The dataset does not contain "
                "price information."
            )


        search_results = search_results.copy()


        search_results["price"] = pd.to_numeric(
            search_results["price"],
            errors="coerce"
        )


        search_results = search_results.dropna(
            subset=["price"]
        )


        if search_results.empty:

            return (
                "I could not find products "
                "with valid prices."
            )


        cheapest = search_results.loc[
            search_results[
                "price"
            ].idxmin()
        ]


        product_name = cheapest.get(
            "product_name",
            "the product"
        )


        price = cheapest[
            "price"
        ]


        return (
            f"The cheapest {keyword} "
            f"is '{product_name}' "
            f"at ₹{price}."
        )


    # ========================================================
    # MOST REVIEWED
    # ========================================================

    if (
        "most reviews" in query
        or "most reviewed" in query
        or "popular" in query
    ):

        if "review_count" not in search_results.columns:

            return (
                "The dataset does not contain "
                "review information."
            )


        search_results = search_results.copy()


        search_results["review_count"] = pd.to_numeric(
            search_results["review_count"],
            errors="coerce"
        )


        search_results = search_results.dropna(
            subset=["review_count"]
        )


        if search_results.empty:

            return (
                "I could not find review information."
            )


        popular_product = search_results.loc[
            search_results[
                "review_count"
            ].idxmax()
        ]


        product_name = popular_product.get(
            "product_name",
            "the product"
        )


        reviews = popular_product[
            "review_count"
        ]


        return (
            f"The most reviewed {keyword} "
            f"is '{product_name}' "
            f"with {int(reviews)} reviews."
        )


    # ========================================================
    # STOCK INFORMATION
    # ========================================================

    if (
        "in stock" in query
        or "available" in query
        or "stock" in query
    ):

        if "stock_quantity" not in search_results.columns:

            return (
                "The dataset does not contain "
                "stock information."
            )


        search_results = search_results.copy()


        search_results["stock_quantity"] = pd.to_numeric(
            search_results["stock_quantity"],
            errors="coerce"
        )


        total_stock = search_results[
            "stock_quantity"
        ].fillna(0).sum()


        return (
            f"I found {len(search_results)} "
            f"{keyword} product(s). "
            f"The total available stock "
            f"across these products is "
            f"{int(total_stock)} units."
        )


    # ========================================================
    # BRAND INFORMATION
    # ========================================================

    if "brand" in query:

        if "brand" not in search_results.columns:

            return (
                "Brand information is "
                "not available."
            )


        brands = (
            search_results["brand"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        if not brands:

            return (
                "I could not find brand information."
            )


        brand_text = ", ".join(
            brands[:10]
        )


        return (
            f"The available {keyword} "
            f"products include these brands: "
            f"{brand_text}."
        )


    # ========================================================
    # GENERAL RESPONSE
    # ========================================================

    return (
        f"I found {len(search_results)} "
        f"product(s) related to '{keyword}'. "
        "I have displayed suitable "
        "recommendations below."
    )