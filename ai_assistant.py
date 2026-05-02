import requests
import API
from speech import speak
from gui import update_output_text

# --- AI Assistant API ---
def mini_ai_assistant(command):
    API_KEY = API.GROQ_API_KEY
    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    conversation_history = [{"role": "system", "content": "You are Mini AI, a helpful assistant."}]
    def ask_question(question):
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        conversation_history.append({"role": "user", "content": question})
        payload = {"model": "llama-3.3-70b-versatile", "messages": conversation_history}
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": answer})
            return answer
        else:
            return f"Error: {response.status_code}, {response.text}"

    formatted_input = f"suppose you are Mini, my AI assistant\nThe question is:\n{command}\nAnswer in short and easy language.when you need listing, Don't answer using * on the behalf of this you can use 1st, 2nd and so no."
    response = ask_question(formatted_input)
    update_output_text("Answer: " + response)
    speak(response)