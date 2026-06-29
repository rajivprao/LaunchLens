from app.graphs.state import LaunchLensState
from app.services.oxylabs_service import OxylabsService
import json 

async def demand_research_node(
    state: LaunchLensState
):

    idea_context = state["idea_context"]
    demand_data = {}
    
    # DemandResearchAgent
    oxylab = OxylabsService()

    search_results = await oxylab.amazon_search(idea_context['search_keywords'][0])
    demand_data = parse_amazon_search(search_results)

    return {"demand_research":demand_data}


def parse_amazon_search(data):
    search_data = {}

    refinements = data.get('results',[])[0].get('content',{}).get('refinements',{})
    results = data.get('results',[])[0].get('content',{}).get('results',{})

    refinement = {}
    result = {}
    result_type = []

    for rows in refinements:
        row_data = []
        for row in refinements[rows]:
            row_data.append(row["name"])
        refinement[rows] = row_data
    
    for rows in results:
        row_data = {}
        result_type = []
        for row in results[rows]:
            row_data = {"asin": row.get("asin"),"price": row.get("price"),"rating": row.get("rating"),
                    "title": row.get("title"),"reviews_count" : row.get("reviews_count")}            
            result_type.append(row_data)
        result[rows] = result_type
    
    search_data["refinements"] = refinement
    search_data["results"] = result

    return search_data

