from app.graphs.state import LaunchLensState


async def summary_node(
    state: LaunchLensState
):

    report = f"""
Verdict:
{state['verdict']['decision']}

Confidence:
{state['verdict']['confidence']}

Positioning:
{state['opportunity_analysis']['positioning']}

Price Band:
{state['opportunity_analysis']['price_band']}
"""

    return {
        "final_report": report
    }