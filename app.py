import pandas as pd
import streamlit as st

from src.product_search import search_products

from src.recommender import (
    filter_by_price,
    recommend_products
)

from src.product_details import (
    get_product_details
)

from src.comparison import (
    compare_products,
    create_comparison_table,
    compare_summary
)

from src.ai_agent import (
    run_agent,
    answer_customer_question
)

from src.customer_data import (
    load_customer_data,
    get_dataset_summary
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Commerce Agent",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

@st.cache_data
def load_products():

    try:

        return pd.read_csv(
            "data/products.csv"
        )

    except FileNotFoundError:

        st.error(
            "❌ data/products.csv was not found."
        )

        st.stop()

    except Exception as error:

        st.error(
            f"❌ Error loading products.csv: {error}"
        )

        st.stop()


products = load_products()


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

customer_data = load_customer_data()


# ============================================================
# TITLE
# ============================================================

st.title("🛍️ AI Commerce Agent")

st.write(
    "AI-powered product search, recommendations, "
    "comparison and customer assistance."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "🏠 Home",
        "🔎 Product Search",
        "⭐ Recommendations",
        "📦 Product Details",
        "⚖️ Compare Products",
        "🤖 AI Customer Assistant",
        "📊 Customer Data"
    ]
)


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.header("Welcome to AI Commerce Agent 🛍️")

    st.write(
        "This application helps customers discover "
        "products using natural-language requests."
    )

    st.write("### Main Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Products",
            len(products)
        )

    with col2:

        st.metric(
            "Product Columns",
            len(products.columns)
        )

    with col3:

        summary = get_dataset_summary(
            customer_data
        )

        total_customer_records = sum(
            summary.values()
        )

        st.metric(
            "Customer Records",
            total_customer_records
        )

    st.markdown("---")

    st.write("### 🚀 What this project can do")

    st.write(
        """
        - 🔎 Search products
        - 💰 Filter products by budget
        - ⭐ Recommend products
        - 📦 Show product details
        - ⚖️ Compare products
        - 🤖 Understand customer requests
        - 🛒 Use purchase data
        - ⭐ Use review data
        - 👤 Use customer data
        """
    )


# ============================================================
# PRODUCT SEARCH
# ============================================================

elif page == "🔎 Product Search":

    st.header("🔎 Product Search")

    search_text = st.text_input(
        "Enter a product name or keyword:",
        placeholder="Example: laptop"
    )

    max_price = st.number_input(
        "Maximum budget (₹)",
        min_value=0.0,
        value=60000.0,
        step=1000.0
    )

    search_button = st.button(
        "🔎 Search Products"
    )

    if search_button:

        if not search_text:

            st.warning(
                "Please enter a product keyword."
            )

        else:

            results = search_products(
                products,
                search_text
            )

            results = filter_by_price(
                results,
                max_price
            )

            st.subheader(
                "🔎 Search Results"
            )

            if results.empty:

                st.warning(
                    "No products found within your budget."
                )

            else:

                st.success(
                    f"Found {len(results)} product(s)."
                )

                st.dataframe(
                    results,
                    use_container_width=True
                )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "⭐ Recommendations":

    st.header("⭐ Product Recommendations")

    search_text = st.text_input(
        "What product are you looking for?",
        placeholder="Example: laptop"
    )

    max_price = st.number_input(
        "Maximum budget (₹)",
        min_value=0.0,
        value=60000.0,
        step=1000.0
    )

    recommend_button = st.button(
        "⭐ Recommend Products"
    )

    if recommend_button:

        if not search_text:

            st.warning(
                "Please enter a product keyword."
            )

        else:

            results = search_products(
                products,
                search_text
            )

            results = filter_by_price(
                results,
                max_price
            )

            recommendations = recommend_products(
                results,
                max_price=max_price,
                top_n=5
            )

            if recommendations.empty:

                st.warning(
                    "No suitable products found."
                )

            else:

                for _, product in recommendations.iterrows():

                    st.markdown("---")

                    st.write(
                        f"### 🛍️ "
                        f"{product.get('product_name', 'Product')}"
                    )

                    if "price" in product.index:

                        st.write(
                            f"💰 **Price:** ₹{product['price']}"
                        )

                    if "brand" in product.index:

                        st.write(
                            f"🏷️ **Brand:** {product['brand']}"
                        )

                    if "category" in product.index:

                        st.write(
                            f"📂 **Category:** {product['category']}"
                        )

                    if "rating_avg" in product.index:

                        st.write(
                            f"⭐ **Rating:** "
                            f"{product['rating_avg']}"
                        )

                    if "review_count" in product.index:

                        st.write(
                            f"💬 **Reviews:** "
                            f"{product['review_count']}"
                        )

                    if "stock_quantity" in product.index:

                        st.write(
                            f"📦 **Stock:** "
                            f"{product['stock_quantity']}"
                        )


# ============================================================
# PRODUCT DETAILS
# ============================================================

elif page == "📦 Product Details":

    st.header("📦 Product Details")

    product_id = st.text_input(
        "Enter Product ID:"
    )

    details_button = st.button(
        "📦 Show Details"
    )

    if details_button:

        if not product_id:

            st.warning(
                "Please enter a Product ID."
            )

        else:

            product = get_product_details(
                products,
                product_id
            )

            if product is None:

                st.error(
                    "❌ Product ID not found."
                )

            else:

                st.success(
                    "Product found!"
                )

                for column in product.index:

                    st.write(
                        f"**{column}:** "
                        f"{product[column]}"
                    )


# ============================================================
# COMPARE PRODUCTS
# ============================================================

elif page == "⚖️ Compare Products":

    st.header("⚖️ Compare Products")

    product_name_1 = st.text_input(
        "First Product Name:"
    )

    product_name_2 = st.text_input(
        "Second Product Name:"
    )

    compare_button = st.button(
        "⚖️ Compare Products"
    )

    if compare_button:

        if not product_name_1 or not product_name_2:

            st.warning(
                "Please enter both product names."
            )

        else:

            product_1, product_2 = compare_products(
                products,
                product_name_1,
                product_name_2
            )

            if product_1 is None:

                st.error(
                    "❌ First product was not found."
                )

            elif product_2 is None:

                st.error(
                    "❌ Second product was not found."
                )

            else:

                comparison = create_comparison_table(
                    product_1,
                    product_2
                )

                st.dataframe(
                    comparison,
                    use_container_width=True
                )

                st.subheader(
                    "📊 Comparison Summary"
                )

                st.write(
                    compare_summary(
                        product_1,
                        product_2
                    )
                )


# ============================================================
# AI CUSTOMER ASSISTANT
# ============================================================

elif page == "🤖 AI Customer Assistant":

    st.header("🤖 AI Customer Assistant")

    st.write(
        "Tell me what you are looking for."
    )

    user_query = st.text_input(
        "Customer request:",
        placeholder=(
            "Example: Recommend me a laptop under 50000"
        )
    )

    assistant_button = st.button(
        "🤖 Ask Assistant"
    )

    if assistant_button:

        if not user_query:

            st.warning(
                "Please enter a customer request."
            )

        else:

            result, recommendations = run_agent(
                user_query,
                products
            )

            st.subheader(
                "🤖 Understanding Your Request"
            )

            st.write(
                f"**Intent:** {result['intent']}"
            )

            st.write(
                f"**Product Keyword:** "
                f"{result['keyword']}"
            )

            if result["budget"] is not None:

                st.write(
                    f"**Detected Budget:** "
                    f"₹{result['budget']}"
                )

            else:

                st.write(
                    "**No budget detected.**"
                )

            answer = answer_customer_question(
                user_query,
                products
            )

            st.info(answer)

            st.subheader(
                "⭐ Recommended Products"
            )

            if recommendations.empty:

                st.warning(
                    "No suitable products found."
                )

            else:

                for _, product in recommendations.iterrows():

                    st.markdown("---")

                    st.write(
                        f"### 🛍️ "
                        f"{product.get('product_name', 'Product')}"
                    )

                    if "price" in product.index:

                        st.write(
                            f"💰 **Price:** "
                            f"₹{product['price']}"
                        )

                    if "brand" in product.index:

                        st.write(
                            f"🏷️ **Brand:** "
                            f"{product['brand']}"
                        )

                    if "category" in product.index:

                        st.write(
                            f"📂 **Category:** "
                            f"{product['category']}"
                        )

                    if "rating_avg" in product.index:

                        st.write(
                            f"⭐ **Rating:** "
                            f"{product['rating_avg']}"
                        )

                    if "review_count" in product.index:

                        st.write(
                            f"💬 **Reviews:** "
                            f"{product['review_count']}"
                        )


# ============================================================
# CUSTOMER DATA
# ============================================================

elif page == "📊 Customer Data":

    st.header("📊 Customer & E-commerce Data")

    summary = get_dataset_summary(
        customer_data
    )

    st.write(
        "These datasets will be used later "
        "to make recommendations more personalized."
    )

    for dataset_name, record_count in summary.items():

        st.write(
            f"**{dataset_name}.csv:** "
            f"{record_count} records"
        )

    st.markdown("---")

    dataset_choice = st.selectbox(
        "Choose a dataset to preview:",
        list(customer_data.keys())
    )

    selected_data = customer_data[
        dataset_choice
    ]

    if selected_data.empty:

        st.warning(
            f"{dataset_choice}.csv "
            "could not be loaded or is empty."
        )

    else:

        st.write(
            f"### {dataset_choice}.csv"
        )

        st.dataframe(
            selected_data.head(20),
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI Commerce Agent | "
    "Track 8 – AI Growth & Agentic Commerce"
)