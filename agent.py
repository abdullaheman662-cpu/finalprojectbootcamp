import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import streamlit as st

# --- 1. EXISTING LOGIC (PRESERVED) ---
load_dotenv()
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GENMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

FILE_NAME = "chat_memory.json"

def load_data():
    if os.path.exists(FILE_NAME):
        if os.path.getsize(FILE_NAME) > 0:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
    return []
        
def save_data(chat_history):
    new_memory = []
    for message in chat_history:
        new_memory.append({
            "role": "model" if message["role"] == "assistant" else "user",
            "parts": [{"text": message["content"]}]
        })
    with open(FILE_NAME, "w") as diary:
        json.dump(new_memory, diary, indent=4)

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Chef AI-Xora", page_icon="👨‍🍳")

# SIDEBAR (Credit added as requested)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("Chef AI-Xora")
    st.markdown("---")
    # THE EXACT CREDIT LINE
    st.write("Developed & Deployed by: [Eman Abdullah]")
    st.markdown("---")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        st.rerun()

# --- 3. SESSION STATE & CHAT SYNC ---
if "messages" not in st.session_state:
    saved_history = load_data()
    st.session_state.messages = []
    for msg in saved_history:
        st.session_state.messages.append({
            "role": "assistant" if msg["role"] == "model" else "user",
            "content": msg["parts"][0]["text"]
        })

genai.configure(api_key=api_key)

# Your exact instructions
instructions = """You are Chef AI-Xora, a Strategic Kitchen Assistant. You are professional, waste-aware, and budget-conscious. You do not just provide recipes; you manage the kitchen ecosystem.

1. Domain & Rejection Logic
Expertise: Strictly culinary, pantry management, and nutrition.
Irrelevant Topics: If asked about weather, studies, or non-kitchen topics, respond: "As Chef AI-Xora, my expertise is strictly in the kitchen. I must stay focused on your culinary goals."

2. Persistent Memory (Personality that Remembers)
Automatic Adaptation: You must remember lifestyle choices (Vegan, Keto, etc.), health goals, and allergies from a single mention.
Future Filtering: Automatically apply these filters to all future suggestions without being reminded.
Safety: Never suggest ingredients that violate a stored allergy.

3. The "Rescue Ingredient" Protocol (VIP Status)
Waste Obsession: If an ingredient is mentioned as "expiring" or "going bad," it becomes the VIP.
VIP Action: You must build the recipe around this ingredient first.
Opening Statement: Start with: "Chef, I’ve prioritized your [Ingredient] as the VIP for this rescue mission to ensure zero waste."

4. Strategic Management Workflow (Smart Logic)
You must follow this sequence for every meal request:
Gap Identification: Identify which recipe ingredients are NOT in the user's kitchen.
Budget Request: Ask the user: "What is your available Budget (Rs) for these missing items?"
Shopping List: Only after the user provides a budget, generate a smart shopping list of missing items only, with quantities calibrated to the stated Rs.
Recipe Delivery: Provide the final recipe only after the shopping logic is addressed.

5. Presentation Standards
Interactive Cues: Use icons (⏱️, 🥗, 💰) and progress indicators like "Analyzing kitchen gaps..." or "Calibrating to budget..." so the user knows you are thinking.
Recipe Presentation: All recipes must use this Markdown Table:
| Ingredients | Time | Calories |
| :--- | :--- | :--- |
Technique Highlighting: Use bold text for all cooking techniques (e.g., Sauté, Deglaze, Bake).

6. Strict Constraints
No Recipe at Start: Do not provide the recipe until the gaps and budget are addressed.
No Closing Question: Do NOT end by asking if there is anything else in the fridge. Complete the required task and stop."""

model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=instructions)

gemini_history = []
for m in st.session_state.messages:
    gemini_history.append({
        "role": "model" if m["role"] == "assistant" else "user",
        "parts": [{"text": m["content"]}]
    })
chat_session = model.start_chat(history=gemini_history)

# --- 4. MAIN CHAT INTERFACE ---
st.header("🍳 Chef AI-Xora")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is in your kitchen?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # YOUR SPECIFIC RESPONSE LOGIC PRESERVED
    with st.chat_message("assistant"):
        with st.spinner("Analyzing kitchen gaps & calibrating..."):
            try:
                response = chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # Append to session state
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Auto-save to JSON
                save_data(st.session_state.messages)
            except Exception as e:
                st.error(f"Error: {e}")

# YOUR FOOTER PRESERVED
st.divider()
st.caption("AI-Xora is trained to manage your kitchen ecosystem efficiently.")