import streamlit as st
from services.amazon_api import search_products, get_reviews, extract_products, extract_reviews
from services.summarizer import generate_review_summary, generate_comparison_summary

st.set_page_config(
    page_title="Compare Products",
    page_icon="⚖️",
    layout="wide"
)

with st.sidebar:
    st.image("assets/reviewnest_logo.png", width=190)
    st.markdown("###")
    st.page_link("0_Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Search_Reviews.py", label="Search Reviews", icon="🔍")
    st.page_link("pages/2_Compare_Products.py", label="Compare Products", icon="⚖️")

st.title("⚖️ Compare Products")
st.write("Search two products and compare them side by side.")

product_name_1 = st.text_input(
    "Enter first product name",
    placeholder="Example: iPhone 15"
)

product_name_2 = st.text_input(
    "Enter second product name",
    placeholder="Example: Samsung Galaxy S24"
)

def get_product_selection(product_name, key_name):
    if not product_name:
        return None

    data = search_products(product_name)
    products = extract_products(data)

    if not products:
        st.warning(f"No products found for {product_name}")
        return None

    product_options = []
    product_map = {}

    for product in products[:10]:
        title = product.get("product_title", "No title")
        price = product.get("product_price", "Price not available")
        rating = product.get("product_star_rating", "No rating")

        label = f"{title} | {price} | Rating: {rating}"
        product_options.append(label)
        product_map[label] = product

    selected_label = st.selectbox(
        f"Choose product for {product_name}",
        product_options,
        key=key_name
    )

    return product_map[selected_label]

if product_name_1 and product_name_2:
    try:
        selected_product_1 = get_product_selection(product_name_1, "product_1")
        selected_product_2 = get_product_selection(product_name_2, "product_2")

        if selected_product_1 and selected_product_2:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("## Product 1")
                image_url = selected_product_1.get("product_photo")
                if image_url:
                    st.image(image_url, use_container_width=True)
                else:
                    st.info("No image available")

                st.markdown(f"### {selected_product_1.get('product_title', 'No title')}")
                st.write(f"**Price:** {selected_product_1.get('product_price', 'Price not available')}")
                st.write(f"**Rating:** {selected_product_1.get('product_star_rating', 'No rating')}")
                st.write(f"**ASIN:** {selected_product_1.get('asin', 'No ASIN')}")

                url_1 = selected_product_1.get("product_url")
                if url_1:
                    st.markdown(f"[Open Product 1 Page]({url_1})")

            with col2:
                st.markdown("## Product 2")
                image_url = selected_product_2.get("product_photo")
                if image_url:
                    st.image(image_url, use_container_width=True)
                else:
                    st.info("No image available")

                st.markdown(f"### {selected_product_2.get('product_title', 'No title')}")
                st.write(f"**Price:** {selected_product_2.get('product_price', 'Price not available')}")
                st.write(f"**Rating:** {selected_product_2.get('product_star_rating', 'No rating')}")
                st.write(f"**ASIN:** {selected_product_2.get('asin', 'No ASIN')}")

                url_2 = selected_product_2.get("product_url")
                if url_2:
                    st.markdown(f"[Open Product 2 Page]({url_2})")

            if st.button("Compare Reviews", use_container_width=True):
                asin_1 = selected_product_1.get("asin")
                asin_2 = selected_product_2.get("asin")

                if not asin_1 or not asin_2:
                    st.error("One of the selected products does not have an ASIN.")
                else:
                    reviews_1 = extract_reviews(get_reviews(asin_1))
                    reviews_2 = extract_reviews(get_reviews(asin_2))

                    summary_1 = generate_review_summary(reviews_1)
                    summary_2 = generate_review_summary(reviews_2)

                    product_1_title = selected_product_1.get("product_title", "Product 1")
                    product_2_title = selected_product_2.get("product_title", "Product 2")

                    comparison_text = generate_comparison_summary(
                        product_1_title,
                        product_2_title,
                        summary_1,
                        summary_2
                    )

                    st.markdown("## Comparison Dashboard")

                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        st.metric("Product 1 Reviews", len(reviews_1))
                    with metric_col2:
                        st.metric("Product 2 Reviews", len(reviews_2))
                    with metric_col3:
                        st.metric("Product 1 Positive", summary_1["pros_score"])
                    with metric_col4:
                        st.metric("Product 2 Positive", summary_2["pros_score"])

                    st.markdown("## AI Comparison Summary")
                    st.info(comparison_text)

                    compare_col1, compare_col2 = st.columns(2)

                    with compare_col1:
                        st.markdown("## Product 1 Summary")
                        st.success(summary_1["overall"])

                        pros_col, cons_col = st.columns(2)
                        with pros_col:
                            st.markdown("### ✅ Pros")
                            for item in summary_1.get("pros", []):
                                st.markdown(f"- {item}")

                        with cons_col:
                            st.markdown("### ⚠️ Cons")
                            for item in summary_1.get("cons", []):
                                st.markdown(f"- {item}")

                    with compare_col2:
                        st.markdown("## Product 2 Summary")
                        st.success(summary_2["overall"])

                        pros_col, cons_col = st.columns(2)
                        with pros_col:
                            st.markdown("### ✅ Pros")
                            for item in summary_2.get("pros", []):
                                st.markdown(f"- {item}")

                        with cons_col:
                            st.markdown("### ⚠️ Cons")
                            for item in summary_2.get("cons", []):
                                st.markdown(f"- {item}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")