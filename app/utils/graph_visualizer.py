from pathlib import Path
from app.graphs.launchlens_graph import build_graph

def save_graph_image(graph, filename: str):

    output_dir = Path("docs/workflows")
    output_dir.mkdir(parents=True, exist_ok=True)

    image_bytes = graph.get_graph().draw_mermaid_png()

    output_path = output_dir / filename

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"Graph saved to {output_path}")


builder = build_graph()
save_graph_image(builder,"LaunchLensFlow.png")