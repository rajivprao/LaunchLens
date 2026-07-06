from app.prompts.verdict_prompt import VERDICT_PROMPT
from app.graphs.state import LaunchLensState
from app.agents.chat_agent import ChatAgent
import json


user_template = """
Generate the final LaunchLens investment assessment report using the following JSON.

The JSON contains:

- Business idea
  {idea}
- Opportunity analysis and Evidence scorecard
  {opportunity}

Determine the verdict using the scoring rules defined in the system prompt.

Return only valid JSON.
"""

async def verdict_node(state: LaunchLensState):

    idea = state["idea_context"]
    opportunity = state["opportunity_analysis"]
    user_inputs = {"idea":idea,"opportunity":opportunity}

    user_prompt = user_template.format(**user_inputs)

    system_instruction = VERDICT_PROMPT
    llm = ChatAgent()
    response = llm.run(query=user_prompt,system_instruction=system_instruction)
    verdict = json.loads(response)

    return {"verdict":verdict}

