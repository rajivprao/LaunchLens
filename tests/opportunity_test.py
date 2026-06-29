from  app.graphs.nodes.demand_research import demand_research_node
from  app.graphs.nodes.supply_research import supply_research_node
from  app.graphs.nodes.idea_analysis import idea_analysis_node
from  app.graphs.nodes.opportunity_analysis import opportunity_analysis_node
from app.graphs.state import LaunchLensState
import asyncio
import json

# product attribute extraction + search keyword generation

user_state = LaunchLensState()
user_state["user_query"] = "I want to launch a portable cordless mini blender in India under ₹2000. Is there enough demand, and what would make it stand out?"

print("Idea - ",user_state["user_query"])
print("building idea ...")
idea_response = asyncio.run(idea_analysis_node(user_state))
user_state["idea_context"] = idea_response["idea_context"]

print("looking for product in ecom ..")
demand_response = asyncio.run( demand_research_node(user_state))
print("looking for similar product insights ...")
supply_response = asyncio.run( supply_research_node(user_state))
user_state["demand_research"] = demand_response["demand_research"]
user_state["supply_research"] = supply_response["supply_research"]
print("analyzing data....")
opportunity_response = asyncio.run( opportunity_analysis_node(user_state))

print("response is output to tests/opportunity.json")


# Writing JSON data
with open("tests/opportunity.json", "w", encoding="utf-8") as file:
    json.dump(opportunity_response, file, indent=4)


# python -m tests.supply_test
