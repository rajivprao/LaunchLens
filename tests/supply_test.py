from  app.graphs.nodes.supply_research import supply_research_node
from  app.graphs.nodes.idea_analysis import idea_analysis_node
from app.graphs.state import LaunchLensState
import asyncio
import json

# product attribute extraction + search keyword generation

user_state = LaunchLensState()
user_state["user_query"] = "I want to launch a portable cordless mini blender in India under ₹1,500. Is there enough demand, and what would make it stand out?"
idea_response = asyncio.run(idea_analysis_node(user_state))
user_state["idea_context"] = idea_response["idea_context"]
#print(idea_response)
supply_response = asyncio.run( supply_research_node(user_state))
print("response is output to tests/supply.json")


# Writing JSON data
with open("tests/supply.json", "w", encoding="utf-8") as file:
    json.dump(supply_response, file, indent=4)


# python -m tests.supply_test
