import json
from pathlib import Path

MEMORY_FILE = Path(
    "app/memory/chat_history/conversation.jsonl"
)

class JsonMemory:


    def __init__(self, window=20):

        self.window = window



    def add_message(
        self,
        session_id,
        role,
        content
    ):


        record = {

            "session_id": session_id,

            "role": role,

            "content": content

        }


        with open(
            MEMORY_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(record)
                + "\n"
            )



    def get_recent(
        self,
        session_id
    ):


        if not MEMORY_FILE.exists():

            return []


        messages = []


        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:


            for line in f:


                item = json.loads(line)


                if item["session_id"] == session_id:

                    messages.append(item)



        return messages[-(self.window * 2):]
