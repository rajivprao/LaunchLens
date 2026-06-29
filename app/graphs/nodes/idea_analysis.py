from app.graphs.state import LaunchLensState
from app.agents.chat_agent import ChatAgent
import app.prompts.idea_prompt as ideaprompt
import json

# product attribute extraction + search keyword generation

async def idea_analysis_node(
    state: LaunchLensState
):

    query = state["user_query"]

    # TODO:
    # call IdeaAnalysisAgent
    instruction = ideaprompt.IDEA_ANALYSIS_PROMPT
    llm = ChatAgent()
    response = llm.run(query=query,system_instruction=instruction)

    idea = json.loads(response)

    return {"idea_context": idea }
