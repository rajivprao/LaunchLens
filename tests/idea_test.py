from  app.graphs.nodes.idea_analysis import idea_analysis_node
from app.graphs.state import LaunchLensState
import asyncio
import json

# product attribute extraction + search keyword generation

user_state = LaunchLensState()
user_state["user_query"] = "I want to launch a portable cordless mini blender in India under ₹2,000. Is there enough demand, and what would make it stand out?"
response = asyncio.run(idea_analysis_node(user_state))
#print(response)
print("response is output to tests/idea.json")
# python -m tests.idea_test
with open("tests/idea.json", "w", encoding="utf-8") as file:
    json.dump(response, file, indent=4)