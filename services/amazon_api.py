import requests
import streamlit as st

BASE_URL = "https://real-time-amazon-data.p.rapidapi.com"


def get_headers():
    return {
        "x-rapidapi-key": st.secrets["RAPIDAPI_KEY"],
        "x-rapidapi-host": st.secrets["RAPIDAPI_HOST"]
    }


@st.cache_data(ttl=3600)
def search_products(query):
    url = f"{BASE_URL}/search"

    params = {
        "query": query,
        "page": "1",
        "country": "US",
        "sort_by": "RELEVANCE",
        "product_condition": "ALL"
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=20
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=3600)
def get_reviews(asin):
    url = f"{BASE_URL}/product-reviews"

    params = {
        "asin": asin,
        "country": "US",
        "page": "1",
        "sort_by": "TOP_REVIEWS",
        "star_rating": "ALL"
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def extract_products(search_response):
    return search_response.get("data", {}).get("products", [])


def extract_reviews(review_response):
    return review_response.get("data", {}).get("reviews", [])   