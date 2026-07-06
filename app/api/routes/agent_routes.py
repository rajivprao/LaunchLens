from fastapi import APIRouter
from app.graphs import launchlens_graph
from app.memory.conversation_memory import JsonMemory

router = APIRouter()

@router.post("/chat")
async def chat(payload: dict): # 1. Changed to async def
    # 2. Removed the nested evaluate function wrapper
    user_query = payload.get("query")
    if not user_query:
        return {"answer": "⚠️ Error: No query provided in the payload."}

    # 3. Directly await the graph invocation
    result = await launchlens_graph.build_graph().ainvoke({"user_query": user_query})

    # 4. Handle memory
    jm = JsonMemory()        
    jm.add_message(1, 'user', user_query)
    jm.add_message(1, 'assistant', result["final_report"])

    # 5. Return the dictionary directly to the client
    return {"answer": result["final_report"]}
