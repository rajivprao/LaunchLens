import gradio as gr
import requests

custom_css = """
body, html {
    margin: 0;
    padding: 0;
    height: 100vh;
    overflow: hidden;
}
.gradio-container {
    height: 100vh !important;
    max-width: 100% !important;
    display: flex;
    flex-direction: column;
}
/* Flex container to separate title (left) and user name (right) */
.top-bar {
    display: flex;
    justify-content: space-between; 
    align-items: center;
    padding: 15px 30px;
    border-bottom: 1px solid #e0e0e0;
    min-height: 50px;
}
/* Pushes the user name text perfectly to the right edge */
.user-name-right {
    text-align: right;
    font-weight: bold;
    font-size: 1.1em;
}
.chat-container {
    flex-grow: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.chatbot-scroll {
    flex-grow: 1;
    overflow-y: auto !important; 
}
"""

enter_key_js = """
function() {
    const observer = new MutationObserver((mutations) => {
        const textarea = document.querySelector('.chat-container textarea');
        if (textarea && !textarea.dataset.enterBound) {
            textarea.dataset.enterBound = "true";
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault(); 
                    const submitBtn = document.querySelector('.chat-container button.primary');
                    if (submitBtn) {
                        submitBtn.click();
                    }
                }
            });
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}
"""

with gr.Blocks(css=custom_css) as demo:
    user_name_state = gr.State("")

    # --- Step 1: Top Bar (Header + Name Display) ---
    with gr.Row(elem_classes="top-bar"):
        # The main title remains fixed on the left side
        gr.Markdown("## 🚀 LaunchLens Chat Assistant", scale=3)
        # The name display is assigned to the right-aligned CSS class
        name_display = gr.Markdown(visible=False, elem_classes="user-name-right", scale=1)

    # --- Step 2: Welcome / Name Input Overlay ---
    with gr.Column(visible=True) as name_prompt_container:
        gr.Markdown("# Welcome! Please enter your name to begin.")
        name_input = gr.Textbox(label="Your Name", placeholder="John Doe", interactive=True)
        name_submit_btn = gr.Button("Submit", variant="primary")

    # --- Step 3: Main Chat Interface ---
    with gr.Column(visible=False, elem_classes="chat-container") as chat_container:
        chatbot = gr.Chatbot(elem_classes="chatbot-scroll", scale=1)
        
        with gr.Row():
            msg = gr.Textbox(
                scale=9,
                show_label=False,
                placeholder="Type your message here and press Enter...",
                lines=2,
                max_lines=2,
                container=False,
                submit_btn=False
            )
            submit_btn = gr.Button("Submit", scale=1, variant="primary")

    # --- Logic / Event Handlers ---
    def handle_name_submit(name):
        if not name.strip():
            return gr.update(), gr.update(), gr.update(visible=False), ""
        welcome_msg = f"👤 **Logged in as:** {name}"
        return (
            gr.update(visible=False), 
            gr.update(visible=True), 
            gr.update(value=welcome_msg, visible=True), 
            name
        )

    name_submit_btn.click(handle_name_submit, [name_input], [name_prompt_container, chat_container, name_display, user_name_state])
    name_input.submit(handle_name_submit, [name_input], [name_prompt_container, chat_container, name_display, user_name_state])

    demo.load(None, None, None, js=enter_key_js)

    # --- API Integration ---
    def call_chat_api(user_message, history):
        if not user_message.strip():
            return "", history

        history.append({"role": "user", "content": user_message})
        
        api_url = "http://localhost:8000/chat"
        payload = {"query": user_message}
        
        try:
            response = requests.post(api_url, json=payload, timeout=30)
            if response.status_code == 200:
                bot_reply = response.json().get("answer", "⚠️ Key 'answer' missing from response.")
            else:
                bot_reply = f"⚠️ Error: Backend server returned status {response.status_code}"
        except requests.exceptions.RequestException as e:
            bot_reply = f"⚠️ Failed to reach backend: {e}"

        history.append({"role": "assistant", "content": bot_reply})
        return "", history

    submit_btn.click(call_chat_api, [msg, chatbot], [msg, chatbot])
    msg.submit(call_chat_api, [msg, chatbot], [msg, chatbot])

demo.launch()


"""
import gradio as gr
import requests


def ask_agent(message, history):

    try:

        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": message}
        )

        return response.json()["answer"]

    except Exception as e:

        return str(e)


demo = gr.ChatInterface(
    fn=ask_agent,
    title="🚀 Launch Lens Research Assistant",
    #type="messages"
)

demo.launch()
"""

"""
import gradio as gr


def chat(message, history):

    history = history or []

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": f"You said: {message}"
        }
    )

    return "", history


with gr.Blocks(title="Launch Lens") as demo:

    gr.Markdown("# 🚀 Launch Lens Research Assistant")

    chatbot = gr.Chatbot(
        show_label=False
    )

    msg = gr.Textbox(
        placeholder="Ask something..."
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

demo.launch()
"""