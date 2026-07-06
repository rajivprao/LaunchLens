from app.graphs.state import LaunchLensState


async def summary_node(
    state: LaunchLensState
):

    return {
        "final_report": state["verdict"]["report_markdown"]
    }
