from app.graphs.state import LaunchLensState
import app.prompts.opportunity_prompt as op
from app.agents.chat_agent import ChatAgent
import json

user_template = """
Analyze the following market research for the startup idea.

STARTUP IDEA

{idea_context}

MARKET RESEARCH

{market_evidence}

Use only the supplied information.

Return the JSON defined in the system instructions.
"""

async def opportunity_analysis_node(
    state: LaunchLensState
):

    idea_context = state["idea_context"]
    demand = state["demand_research"]
    supply = state["supply_research"]
    market_evidence = {"source1":demand,"source2":supply}
    user_inputs = {"idea_context":idea_context,"market_evidence":market_evidence}
    # TODO:
    # OpportunityAgent

    user_prompt = user_template.format(**user_inputs)

    system_instruction = op.OPPORTUNITY_ANALYSIS_PROMPT
    llm = ChatAgent()
    response = llm.run(query=user_prompt,system_instruction=system_instruction)

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

