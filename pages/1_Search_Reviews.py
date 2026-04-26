import streamlit as st
from services.amazon_api import search_products, get_reviews, extract_products, extract_reviews
from services.summarizer import generate_review_summary

st.set_page_config(
    page_title="Search Reviews",
    page_icon="🔍",
    layout="wide"
)

with st.sidebar:
    st.image("assets/reviewnest_logo.png", width=190)
    st.markdown("###")
    st.page_link("0_Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Search_Reviews.py", label="Search Reviews", icon="🔍")
    st.page_link("pages/2_Compare_Products.py", label="Compare Products", icon="⚖️")

st.title("🔍 Search Reviews")
st.write("Search for a product, fetch real Amazon reviews, and view a smart summary.")

product_name = st.text_input(
    "Enter product name",
    placeholder="Example: iPhone 15, Nike shoes, PS5 controller"
)

if product_name:
    try:
        data = search_products(product_name)
        products = extract_products(data)

        if not products:
            st.warning("No products found.")
        else:
            st.subheader("Search Results")

            product_options = []
            product_map = {}

            for product in products[:10]:
                title = product.get("product_title", "No title")
                price = product.get("product_price", "Price not available")
                rating = product.get("product_star_rating", "No rating")
                label = f"{title} | {price} | Rating: {rating}"
                product_options.append(label)
                product_map[label] = product

            selected_label = st.selectbox("Choose a product", product_options)
            selected_product = product_map[selected_label]

            st.markdown("## Selected Product")

            col1, col2 = st.columns([1, 2])

            with col1:
                image_url = selected_product.get("product_photo")
                if image_url:
                    st.image(image_url, use_container_width=True)
                else:
                    st.info("No image available")

            with col2:
                st.markdown(f"### {selected_product.get('product_title', 'No title')}")
                st.write(f"**Price:** {selected_product.get('product_price', 'Price not available')}")
                st.write(f"**Rating:** {selected_product.get('product_star_rating', 'No rating')}")
                st.write(f"**ASIN:** {selected_product.get('asin', 'No ASIN')}")

                product_url = selected_product.get("product_url")
                if product_url:
                    st.markdown(f"[Open Product Page]({product_url})")

            if st.button("Fetch Reviews", use_container_width=True):
                asin = selected_product.get("asin")

                if not asin:
                    st.error("No ASIN found for this product.")
                else:
                    review_data = get_reviews(asin)
                    reviews = extract_reviews(review_data)

                    if not reviews:
                        st.warning("No reviews found for this product.")
                    else:
                        summary = generate_review_summary(reviews)

                        st.markdown("## Review Dashboard")

                        metric_col1, metric_col2, metric_col3 = st.columns(3)

                        with metric_col1:
                            st.metric("Total Reviews Fetched", len(reviews))
                        with metric_col2:
                            st.metric("Positive Score", summary["pros_score"])
                        with metric_col3:
                            st.metric("Negative Score", summary["cons_score"])

                        st.success(summary["overall"])

                        pros_col, cons_col = st.columns(2)

                        with pros_col:
                            st.markdown("### ✅ Pros")
                            for item in summary.get("pros", []):
                                st.markdown(f"- {item}")

                        with cons_col:
                            st.markdown("### ⚠️ Cons")
                            for item in summary.get("cons", []):
                                st.markdown(f"- {item}")

                        st.markdown("### Quick Highlights")
                        for point in summary.get("highlights", []):
                            st.markdown(f"- {point}")

                        st.markdown("## Customer Reviews")

                        for i, review in enumerate(reviews[:5], start=1):
                            title = review.get("review_title", "No title")
                            text = review.get("review_comment", "No review text")
                            rating = review.get("review_star_rating", "No rating")
                            author = review.get("review_author", "Anonymous")
                            review_date = review.get("review_date", "No date")

                            with st.container(border=True):
                                st.markdown(f"### Review {i}: {title}")
                                info_col1, info_col2, info_col3 = st.columns(3)

                                with info_col1:
                                    st.write(f"**Rating:** {rating}")
                                with info_col2:
                                    st.write(f"**Author:** {author}")
                                with info_col3:
                                    st.write(f"**Date:** {review_date}")

                                st.write(text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")