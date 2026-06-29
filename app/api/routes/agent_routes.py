from fastapi import APIRouter
#from app.agents.chat_agent import ChatAgent
from app.graphs import launchlens_graph
from app.memory.conversation_memory import JsonMemory

router = APIRouter()

#agent = ChatAgent()
#return agent.run(payload["query"])

   
@router.post("/chat")
def chat(payload: dict):

    async def evaluate(request):

        result = await launchlens_graph.build_graph().ainvoke({"user_query": payload["query"]})

        jm = JsonMemory()        
        jm.add_message(1,'user',payload["query"])
        jm.add_message(1,'assistant',result)

        return result

