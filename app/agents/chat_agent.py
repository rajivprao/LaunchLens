from openai import OpenAI
from app.config.settings import Secrets
from app.memory.conversation_memory import JsonMemory

class ChatAgent:

    def run(self, query: str, system_instruction:str,with_chat_history=False):

        secrets = Secrets()

        
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = secrets.NVIDIA_API_KEY
        )
        
        """
        client = OpenAI(
            base_url = "https://googleapis.com",
            api_key = secrets.GEMINI_API_KEY
        )
        """
        chat_history = []

        if with_chat_history:
            jm = JsonMemory()
            chat_history = jm.get_recent(1)
            
        chat_history.append({"role": "system", "content": system_instruction})
        chat_history.append({"role": "user", "content": query})        

        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
            #model = "gemini-2.5-flash",
            messages=chat_history,  
            temperature=1.00,
            top_p=0.01,
            max_tokens=1024,
            stream=False
        )

        response = completion.choices[0].message.content  

        return response    

    