from langgraph.graph import (
    START,
    END,
    StateGraph
)

from app.graphs.state import (
    LaunchLensState
)

from app.graphs.nodes.idea_analysis import (
    idea_analysis_node
)

from app.graphs.nodes.demand_research import (
    demand_research_node
)

from app.graphs.nodes.supply_research import (
    supply_research_node
)

from app.graphs.nodes.opportunity_analysis import (
    opportunity_analysis_node
)

from app.graphs.nodes.verdict import (
    verdict_node
)

from app.graphs.nodes.summary import (
    summary_node
)


def build_graph():

    builder = StateGraph(
        LaunchLensState
    )

    builder.add_node(
        "idea_analysis",
        idea_analysis_node
    )

    builder.add_node(
        "demand_research",
        demand_research_node
    )

    builder.add_node(
        "supply_research",
        supply_research_node
    )

    builder.add_node(
        "opportunity_analysis",
        opportunity_analysis_node
    )

    builder.add_node(
        "verdict",
        verdict_node
    )

    builder.add_node(
        "summary",
        summary_node
    )

    builder.add_edge(
        START,
        "idea_analysis"
    )

    builder.add_edge(
        "idea_analysis",
        "demand_research"
    )

    builder.add_edge(
        "idea_analysis",
        "supply_research"
    )

    builder.add_edge(
        "demand_research",
        "opportunity_analysis"
    )

    builder.add_edge(
        "supply_research",
        "opportunity_analysis"
    )

    builder.add_edge(
        "opportunity_analysis",
        "verdict"
    )

    builder.add_edge(
        "verdict",
        "summary"
    )

    builder.add_edge(
        "summary",
        END
    )

    return builder.compile()