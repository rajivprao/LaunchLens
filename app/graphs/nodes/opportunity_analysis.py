from app.graphs.state import LaunchLensState
import app.prompts.opportunity_prompt as op
from app.agents.chat_agent import ChatAgent
import json
import pandas as pd


user_template = """
Analyze the following market research for the startup idea.

STARTUP IDEA

{idea_context}

MARKET RESEARCH

{market_evidence}

Use only the supplied information.

Return the JSON defined in the system instructions.
"""

def transformAmazonData(amazon_dict):
    """
    
    """
    results_summary = {}
    amazon_result = {}
    results_dict = amazon_dict.get("results",{})

    for raw_listings in results_dict:

        df = pd.DataFrame(results_dict[raw_listings])
        
        if len(df) == 0:
            continue        

        # 1. HARD MARKET BOUNDARIES (No exaggeration, just limits)
        min_price = df["price"].min()
        max_price = df["price"].max()

        # 2. THE VOLUMETRIC CENTER OF MASS
        # Instead of guessing sales, we sum up where the reviews are concentrated
        total_sample_reviews = df["reviews_count"].sum()

        # Find the midpoint price of your sample
        price_midpoint = (max_price + min_price) / 2

        # Split the review counts strictly based on that midpoint
        below_midpoint_reviews = df[df["price"] <= price_midpoint]["reviews_count"].sum()
        above_midpoint_reviews = df[df["price"] > price_midpoint]["reviews_count"].sum()

        # Determine where the volume bias sits
        if below_midpoint_reviews > above_midpoint_reviews:
            volume_bias = f"Lower Half (Below ₹{price_midpoint:.0f})"
        elif above_midpoint_reviews > below_midpoint_reviews:
            volume_bias = f"Upper Half (Above ₹{price_midpoint:.0f})"
        else:
            volume_bias = "Equally Distributed"

        # 3. RATING PROFILE OF THE MARKET LEADER
        # Find the entity that has managed to capture the most attention/reviews
        leader_row = df.loc[df["reviews_count"].idxmax()]

        pulse_packet = {
            "absolute_price_floor": int(min_price),
            "absolute_price_ceiling": int(max_price),
            "sample_total_reviews": int(total_sample_reviews),
            "where_the_volume_sits": volume_bias,
            "most_reviewed_product_asin": leader_row["title"],
            "most_reviewed_product_rating": float(leader_row["rating"])
        }

        results_summary[raw_listings] = pulse_packet
    
    amazon_result = {"results":results_summary}
    if "refinements" in amazon_dict: 
        {"filters":amazon_dict["refinements"]}
    
    return amazon_result

import re
import numpy as np
import pandas as pd


def clean_currency_string(price_str: str) -> float:
    """Helper to remove currency symbols, hidden characters, commas,

    and convert price strings safely to numeric float values.
    """
    if not price_str or not isinstance(price_str, str):
        return 0.0
    # Keep only digits and decimal dots
    cleaned = re.sub(r"[^\d.]", "", price_str)
    return float(cleaned) if cleaned else 0.0


def extract_discount_from_anchor(original_price_str: str, current_price: float) -> float:
    """Helper to catch discount rates from text fields like '72% off₹7,999'

    or calculate it implicitly if old values are found.
    """
    if not original_price_str or not isinstance(original_price_str, str):
        return 0.0

    # Look for an explicit percentage signature (e.g., '72% off')
    pct_match = re.search(r"(\d+)%\s*off", original_price_str, re.IGNORECASE)
    if pct_match:
        return float(pct_match.group(1))

    # Alternative: Parse the numerical anchor price and compare mathematically
    cleaned_anchor = re.sub(r"[^\d.]", "", original_price_str.split("₹")[-1])
    if cleaned_anchor:
        old_val = float(cleaned_anchor)
        if old_val > current_price:
            return round(((old_val - current_price) / old_val) * 100, 1)

    return 0.0


def analyze_product_snapshot(raw_product_list: list) -> dict:
    """Processes a collection of e-commerce listings to extract market segments,

    pricing boundaries, merchant footprints, and promotional weights.
    """
    if not raw_product_list:
        return {"error": "Product listing array is empty."}

    cleaned_items = []
    for item in raw_product_list:
        title = item.get("title", "Unknown Product")
        source = item.get("source", "Unknown Retailer")
        current_p = clean_currency_string(item.get("price", "0"))

        # Safe parsing for optional numerical categories
        rating = float(item.get("rating", 0.0)) if item.get("rating") else None
        reviews = int(item.get("reviews", 0)) if item.get("reviews") else 0

        # Calculate discount depth
        discount = extract_discount_from_anchor(
            item.get("original_price", ""), current_p
        )

        cleaned_items.append(
            {
                "title": title,
                "source": source,
                "price": current_p,
                "rating": rating,
                "reviews": reviews,
                "discount_percent": discount,
            }
        )

    df = pd.DataFrame(cleaned_items)

    # 1. Price Calculations
    prices = df["price"].values
    min_p = float(np.min(prices))
    max_p = float(np.max(prices))
    avg_p = float(np.mean(prices))
    median_p = float(np.median(prices))

    # 2. Competitive Landscape Footprints
    total_listings = len(df)
    unique_retailers = df["source"].nunique()
    top_retailer = df["source"].value_counts().index[0]

    # 3. Promotional Distribution
    promotional_items_count = int((df["discount_percent"] > 0).sum())
    avg_market_discount = float(df["discount_percent"].mean())

    # 4. Review Sentiment Weight (Filter out products lacking validation data)
    rated_products = df[df["rating"].notnull()]
    if not rated_products.empty:
        average_consumer_rating = float(rated_products["rating"].mean())
        total_tracked_reviews = int(rated_products["reviews"].sum())
        market_sentiment = (
            "Highly Positive"
            if average_consumer_rating >= 4.2
            else "Moderate" if average_consumer_rating >= 3.0 else "Critical / Poor"
        )
    else:
        average_consumer_rating = None
        total_tracked_reviews = 0
        market_sentiment = "Insufficient Data"

    # 5. Define Market Complexity Status
    if max_p / (min_p if min_p > 0 else 1) > 5:
        market_tier_type = "Highly Fragmented (Wide Budget to Premium Gap)"
    else:
        market_tier_type = "Consolidated / Uniform"

    return {
        "total_observed_listings": total_listings,
        "market_tier_type": market_tier_type,
        "price_min": min_p,
        "price_max": max_p,
        "price_average": round(avg_p, 2),
        "price_median": median_p,
        "unique_retailers_count": unique_retailers,
        "dominant_retailer_source": top_retailer,
        "discounted_listings_count": promotional_items_count,
        "average_calculated_discount_pct": round(avg_market_discount, 1),
        "average_consumer_rating": (
            round(average_consumer_rating, 2)
            if average_consumer_rating
            else None
        ),
        "total_validated_reviews": total_tracked_reviews,
        "market_sentiment_status": market_sentiment,
    }

def transformGoogleData(google_dict):
    google_result = {}
    
    google_search = google_dict.get("google_search")
    google_news = google_dict.get("google_news")
    google_trends = google_dict.get("google_trends")

    transformed_search = {}

    if "questions" in google_search:
        transformed_search["questions"] = google_search["questions"]

    if "ai_overview" in google_search:
        transformed_search["ai_overview"] = google_search["ai_overview"]

    if "related_searches" in google_search:
        transformed_search["related_searches"] = google_search["related_searches"]

    if "immersive_products" in google_search:
        transformed_search["immersive_products"] = analyze_product_snapshot(google_search["immersive_products"])

    transformed_news = []
    for news in google_news[:10]:
        transformed_news.append(news)
    
    transformed_trends = get_trend_insights(google_trends)

    google_result["trends"] = transformed_trends
    google_result["news"] = transformed_news
    google_result["search"] = transformed_search

    return google_result

def _parse_shorthand_google_date(date_str: str) -> str:
    """Helper to convert Google Trend week ranges to a single 'YYYY-MM-DD' start date.

    Handles variations like:
    - 'Jun 29 – Jul 5, 2025' -> '2025-06-29'
    - 'Jul 6 – 12, 2025'     -> '2025-07-06'
    """
    # Split using any form of unicode or standard dash
    parts = re.split(r"[\u2012\u2013\u2014\u2015\-–—]+", date_str)
    parts = [p.strip() for p in parts]

    if len(parts) != 2:
        raise ValueError(f"Could not parse date format: {date_str}")

    start_part, end_part = parts[0], parts[1]

    # Extract the year from whichever part has it (usually the end)
    year_match = re.search(r"\d{4}", date_str)
    if not year_match:
        raise ValueError(f"No 4-digit year found in date string: {date_str}")
    year = year_match.group()

    # Case 1: Start part has both Month and Day (e.g., "Jun 29")
    # Match 3 characters for month followed by digits for day
    if re.match(r"^[A-Za-z]{3}\s+\d+", start_part):
        # If it happens to have a year already due to crossing year boundary
        if "," in start_part:
            dt = pd.to_datetime(start_part)
        else:
            dt = pd.to_datetime(f"{start_part}, {year}")
        return dt.strftime("%Y-%m-%d")

    # Case 2: Start part is just a number (e.g., "6" from "Jul 6 – 12, 2025")
    # We need to borrow the month name from the end part
    else:
        # Get the 3-letter month from the end part (e.g., "Jul" from "Jul 12, 2025")
        month_match = re.search(r"[A-Za-z]{3}", date_str)
        if not month_match:
            raise ValueError(
                f"Could not find a month name in date string: {date_str}"
            )
        month = month_match.group()
        day = start_part  # The left side is just the start day

        dt = pd.to_datetime(f"{month} {day}, {year}")
        return dt.strftime("%Y-%m-%d")


def get_trend_insights(raw_data_list: list) -> dict:
    """Master function: Accepts raw list of Google Trend JSON objects,

    normalizes the messy timeline, evaluates mathematical momentum,
    and returns a structured payload optimized for downstream LLM/Logic nodes.
    """
    if not raw_data_list or len(raw_data_list) < 2:
        return {"error": "Insufficient data points to extract meaningful trends."}

    # 1. Transform raw list into a DataFrame
    df = pd.DataFrame(raw_data_list)

    # 2. Rename expected value column if necessary, map values to float
    val_col = "extracted_value" if "extracted_value" in df.columns else "interest"
    if val_col not in df.columns:
        return {
            "error": "Data must contain an 'extracted_value' or 'interest' metric column."
        }

    # 3. Apply the custom shorthand date parser to construct a true timeline
    try:
        df["timestamp"] = df["date"].apply(_parse_shorthand_google_date)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp").sort_index()
    except Exception as e:
        return {"error": f"Date preprocessing failed: {str(e)}"}

    values = df[val_col].astype(float).values
    n_periods = len(values)

    # 4. Range and Timeline Calculations
    trend_start_date = df.index[0].strftime("%Y-%m-%d")
    trend_end_date = df.index[-1].strftime("%Y-%m-%d")
    total_tracked_days = int((df.index[-1] - df.index[0]).days)

    # 5. Peak and Baseline Metrics
    latest_interest = float(values[-1])
    peak_interest = float(np.max(values))
    peak_idx = int(np.argmax(values))
    days_since_peak = int((df.index[-1] - df.index[peak_idx]).days)
    peak_date = df.index[peak_idx].strftime("%Y-%m-%d")
    average_interest = float(np.mean(values))

    # 6. Trend Slopes & Growth Rates
    x = np.arange(n_periods)
    long_term_slope = float(np.polyfit(x, values, 1)[0])

    fit_line = np.polyval(np.polyfit(x, values, 1), x)
    start_val = fit_line[0]
    growth_rate_percent = (
        float(((fit_line[-1] - start_val) / start_val) * 100)
        if start_val != 0
        else 0.0
    )

    # Short-term momentum calculation (safely defaults if tracking range is short)
    short_span = min(5, n_periods)
    short_term_slope = float(
        np.polyfit(np.arange(short_span), values[-short_span:], 1)[0]
        if short_span > 1
        else 0
    )

    # 7. Volatility Calculations
    volatility_score = (
        float(np.std(values) / average_interest) if average_interest != 0 else 0
    )

    # 8. Categorical State Mappings
    if long_term_slope > 0.1:
        overall_trend = "Growing"
    elif long_term_slope < -0.1:
        overall_trend = "Declining"
    else:
        overall_trend = "Stable / Flat"

    if short_term_slope < -0.5:
        recent_momentum = "Steep Decline"
    elif short_term_slope < -0.05:
        recent_momentum = "Gradual Decay"
    elif short_term_slope > 0.5:
        recent_momentum = "Sharp Surge"
    elif short_term_slope > 0.05:
        recent_momentum = "Steady Climb"
    else:
        recent_momentum = "Stagnant / Flatline"

    if latest_interest >= 75:
        market_interest = "Very High"
    elif latest_interest >= 40:
        market_interest = "Moderate"
    else:
        market_interest = "Low"

    if peak_interest > 0:
        retention_ratio = latest_interest / peak_interest
        if retention_ratio > 0.7:
            interest_persistence = "High"
        elif retention_ratio > 0.3:
            interest_persistence = "Moderate"
        else:
            interest_persistence = "Low"
    else:
        interest_persistence = "None"

    volatility = (
        "High"
        if volatility_score > 0.5
        else "Moderate" if volatility_score > 0.2 else "Low"
    )

    # 9. Streak Monitoring
    # Using a minor rolling window baseline for streak evaluations if the dataset expands
    window_sz = min(3, n_periods)
    ma_diff = (
        df[val_col].rolling(window=window_sz, min_periods=1).mean().diff().fillna(0).values
    )

    current_streak_duration = 0
    current_streak_direction = "Flat"

    if len(ma_diff) >= 2:
        is_up = ma_diff[-1] > 0.01
        is_down = ma_diff[-1] < -0.01

        if is_up:
            current_streak_direction = "Climbing"
            for val in reversed(ma_diff):
                if val > 0:
                    current_streak_duration += 1
                else:
                    break
        elif is_down:
            current_streak_direction = "Declining"
            for val in reversed(ma_diff):
                if val < 0:
                    current_streak_duration += 1
                else:
                    break

    trend_confidence = float(max(0.0, min(1.0, 1.0 - (volatility_score * 0.25))))

    return {
        "trend_start_date": trend_start_date,
        "trend_end_date": trend_end_date,
        "total_tracked_days": total_tracked_days,
        "overall_trend": overall_trend,
        "recent_momentum": recent_momentum,
        "market_interest": market_interest,
        "growth_rate_percent": round(growth_rate_percent, 1),
        "average_interest": round(average_interest, 1),
        "latest_interest": round(latest_interest, 1),
        "peak_interest": round(peak_interest, 1),
        "peak_date": peak_date,
        "days_since_peak": int(days_since_peak),
        "current_streak_direction": current_streak_direction,
        "current_streak_duration": int(current_streak_duration),
        "interest_persistence": interest_persistence,
        "seasonality": "None",
        "volatility": volatility,
        "volatility_score": round(volatility_score, 2),
        "trend_confidence": round(trend_confidence, 2),
    }

async def opportunity_analysis_node(
    state: LaunchLensState
):

    idea_context = state["idea_context"]
    demand = state["demand_research"]
    supply = state["supply_research"]

    transformed_demand = transformAmazonData(demand)
    transformed_supply = transformGoogleData(supply)

    market_evidence = {"AmazonData":transformed_demand,"GoogleData":transformed_supply}
    user_inputs = {"idea_context":idea_context,"market_evidence":market_evidence}

    with open(f"tests/results/market_evidence.json", "w", encoding="utf-8") as file:
        json.dump(market_evidence, file, indent=4)

    # TODO:
    # OpportunityAgent

    user_prompt = user_template.format(**user_inputs)

    system_instruction = op.OPPORTUNITY_ANALYSIS_PROMPT
    llm = ChatAgent()
    response = llm.run(query=user_prompt,system_instruction=system_instruction)
  
    # Open file in append mode ('a')
    with open('tests/opportunity.txt', 'w', encoding='utf-8') as file:
        file.write(response)

    opportunity = json.loads(response)

    return {"opportunity_analysis":opportunity}

    """return {
        "opportunity_analysis": {
            "score": 80,
            "positioning":
                "Inventory forecasting for SMB restaurants",
            "price_band":
                "$49-$199/month",
            "risks": [],
            "opportunities": []
        }
    }"""

