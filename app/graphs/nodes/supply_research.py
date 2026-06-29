from app.graphs.state import LaunchLensState
from app.services.serpapi_service import SerpApiService

async def supply_research_node(
    state: LaunchLensState
):

    idea_context = state["idea_context"]
    supply_research = {}
    search_word = idea_context['product_type'] + " " + idea_context['search_keywords'][0]
    search_trend = idea_context['search_keywords'][0]
    tbs = idea_context['target_price_constraint']

    # SupplyResearchAgent
    serp = SerpApiService()
        
    search_data = await serp.google_search(search_word,tbs=tbs)    
    search_parsed = parse_google_search(search_data)
    supply_research["google_search"] = search_parsed

    news_data = await serp.google_news(search_word)
    news_parsed = parse_google_news(news_data)
    supply_research["google_news"] = news_parsed

    trends_data = await serp.google_trends(search_trend)
    trends_parsed = parse_google_trends(trends_data)
    supply_research["google_trends"] = trends_parsed

    return {"supply_research": supply_research }

def parse_google_search(search_response):

    search_data_processed = {}

    sections = extract_ai_overview_sections(search_response)
    if not sections:
        search_data_processed["ai_overview"] = sections

    if "inline_images" in search_response:
        titles  = [item.get("title") for item in search_response["inline_images"]] 
        sources  = [item.get("source_name") for item in search_response["inline_images"]] 
        search_data_processed["inline_images"] = {"titles":titles,"sources":sources}

    if "related_questions" in search_response:
        questions = [item.get("question") for item in search_response["related_questions"]] 
        search_data_processed["questions"] = questions

    if "organic_results" in search_response:       
        keep_keys = {"snippet", "source", "title"}
        filtered_products = [
            {key: item[key] for key in keep_keys if key in item} 
            for item in search_response["organic_results"]
        ]
        search_data_processed["organic_results"] = filtered_products
    
    if "immersive_products" in search_response:
        keep_keys = {"category", "source", "title","rating","reviews","price","original_price","old_price"}
        filtered_products = [
            {key: item[key] for key in keep_keys if key in item} 
            for item in search_response["immersive_products"]
        ]
        search_data_processed["immersive_products"] = filtered_products

    if "related_searches" in search_response:
        querys = [item.get("query") for item in search_response["related_searches"]]
        search_data_processed["related_searches"] = querys

    return search_data_processed

def parse_google_news(serp_data):
    news_data_processed = []

    for rows in serp_data["news_results"]:
        news_obj = {}
        news_obj["title"] = rows["title"]
        news_obj["source"] = rows["source"]["name"]
        news_data_processed.append(news_obj)

    return news_data_processed

def parse_google_trends(serp_data):
    trends_data_processed = []
    if "interest_over_time" in serp_data:
        trends_data = serp_data["interest_over_time"]
    else: 
        return {}
    for entry in trends_data.get("timeline_data", []):
        # Extract the outer date attribute
        date_val = entry.get("date")
        
        # Loop through each dictionary inside the "values" array
        # If there are multiple items, this loop will handle all of them for the same date
        for val_item in entry.get("values", []):
            trends_data_processed.append({
                "date": date_val,
                "query": val_item.get("query"),
                "extracted_value": val_item.get("extracted_value")
            })

    return trends_data_processed

def extract_ai_overview_sections(response):

    sections = []
    buttons = (response.get("things_to_know", {}).get("buttons", []))  

    for button in buttons:

        section_name = button.get("text", "")
        overview = button.get("ai_overview", {})
        text_blocks = overview.get("text_blocks", [])
        block_text = []

        for block in text_blocks:

            if block.get("snippet"):
                block_text.append(block["snippet"])

            if block.get("type") == "list":

                for item in block.get("list", []):

                    if item.get("title"):
                        block_text.append(item["title"])

                    if item.get("snippet"):
                        block_text.append(item["snippet"])

        sections.append({"section": section_name,"content": block_text})

    return sections