import json
import streamlit as st
from openai import OpenAI


def generate_basic_summary(reviews):
    pros = []
    cons = []

    positive_keywords = [
        "good", "great", "excellent", "amazing", "love",
        "best", "perfect", "awesome", "nice", "satisfied",
        "comfortable", "fast", "useful", "quality"
    ]

    negative_keywords = [
        "bad", "poor", "worst", "hate", "terrible",
        "broken", "waste", "problem", "disappointed", "slow",
        "expensive", "cheap", "difficult", "issue"
    ]

    for review in reviews[:10]:
        text = f"{review.get('review_title', '')} {review.get('review_comment', '')}".strip()
        lower_text = text.lower()

        if any(word in lower_text for word in positive_keywords) and len(pros) < 3:
            pros.append(text[:160])

        if any(word in lower_text for word in negative_keywords) and len(cons) < 3:
            cons.append(text[:160])

    if not pros:
        pros = ["Customers generally liked some aspects of the product."]
    if not cons:
        cons = ["Some users reported mixed or limited concerns."]

    return {
        "overall": "Customer sentiment appears mixed but generally positive.",
        "pros_score": len(pros),
        "cons_score": len(cons),
        "pros": pros[:3],
        "cons": cons[:3],
        "highlights": pros[:2] + cons[:1]
    }


@st.cache_data(ttl=3600)
def generate_review_summary(reviews):
    if not reviews:
        return {
            "overall": "No reviews available.",
            "pros_score": 0,
            "cons_score": 0,
            "pros": [],
            "cons": [],
            "highlights": []
        }

    review_texts = []
    for review in reviews[:10]:
        title = review.get("review_title", "No title")
        text = review.get("review_comment", "No review text")
        rating = review.get("review_star_rating", "No rating")
        review_texts.append(f"Title: {title}\nRating: {rating}\nReview: {text}")

    combined_reviews = "\n\n".join(review_texts)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.responses.create(
            model="gpt-5-mini",
            input=f"""
You are analyzing customer reviews for a product review app.

Based on the reviews below, return ONLY valid JSON in this exact format:

{{
  "overall": "1-2 sentence natural summary",
  "pros_score": 0,
  "cons_score": 0,
  "pros": ["pro 1", "pro 2", "pro 3"],
  "cons": ["con 1", "con 2", "con 3"],
  "highlights": ["highlight 1", "highlight 2", "highlight 3"]
}}

Rules:
- pros_score and cons_score must be integers from 0 to 10
- pros must be specific, short, and based on the reviews
- cons must be specific, short, and based on the reviews
- do not use vague phrases like "mostly positive" unless supported
- keep each pro/con under 12 words
- output JSON only

Reviews:
{combined_reviews}
"""
        )

        text = response.output_text.strip()
        result = json.loads(text)

        return {
            "overall": result.get("overall", "Summary not available."),
            "pros_score": int(result.get("pros_score", 0)),
            "cons_score": int(result.get("cons_score", 0)),
            "pros": result.get("pros", [])[:3],
            "cons": result.get("cons", [])[:3],
            "highlights": result.get("highlights", [])[:3]
        }

    except Exception:
        return generate_basic_summary(reviews)


@st.cache_data(ttl=3600)
def generate_comparison_summary(product_1_name, product_2_name, summary_1, summary_2):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.responses.create(
            model="gpt-5-mini",
            input=f"""
You are comparing two products for a shopping assistant app.

Product 1: {product_1_name}
Summary 1:
- Overall: {summary_1.get('overall')}
- Pros: {summary_1.get('pros')}
- Cons: {summary_1.get('cons')}

Product 2: {product_2_name}
Summary 2:
- Overall: {summary_2.get('overall')}
- Pros: {summary_2.get('pros')}
- Cons: {summary_2.get('cons')}

Write a short comparison in 3 parts:
1. Key difference
2. Which product seems better for what kind of user
3. Final verdict in 1 sentence

Keep it concise and natural.
"""
        )

        return response.output_text.strip()

    except Exception:
        return (
            f"{product_1_name} seems stronger in some areas, while {product_2_name} "
            f"may suit users with different priorities. Choose based on the pros and cons shown above."
        )