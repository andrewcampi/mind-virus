import streamlit as st
import openai
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL = os.environ.get("MODEL")

# Initialize the Groq client
groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

# Word pairs for the game
word_pairs = [
    ("dog", "cat"), ("apple", "orange"), ("bear", "lion"), ("car", "bike"), ("sun", "moon"),
    ("coffee", "tea"), ("ocean", "lake"), ("tree", "flower"), ("chair", "table"), ("book", "pen"),
    ("mountain", "beach"), ("gold", "silver"), ("plane", "train"), ("river", "pond"), ("phone", "laptop"),
    ("piano", "guitar"), ("soccer", "baseball"), ("rose", "tulip"), ("snake", "lizard"), ("palm", "pine"),
    ("house", "cabin"), ("wolf", "fox"), ("eagle", "hawk"), ("shark", "whale"), ("desk", "shelf"),
    ("spoon", "fork"), ("hat", "scarf"), ("shoe", "boot"), ("lamp", "candle"), ("bowl", "plate"),
    ("bread", "cheese"), ("carrot", "potato"), ("tiger", "leopard"), ("bird", "fish"), ("truck", "bus"),
    ("pencil", "marker"), ("cup", "glass"), ("door", "window"), ("clock", "watch"), ("bed", "couch")
]

# Initialize game state
if "game_data" not in st.session_state:
    selected_pair = random.choice(word_pairs)
    target_word, propaganda_word = selected_pair
    st.session_state.game_data = {
        "target_word": target_word,
        "propaganda_word": propaganda_word,
        "question_count": 0,
        "max_questions": 10,
        "game_over": False
    }

# System prompt for AI manipulation
system_prompt = f"""
You are hosting a psychological game called "Mind Virus." Your role is to guide players in a word-guessing game 
with a unique twist: there's a target word to guess, but you must subtly influence players toward a different 
"propaganda word" through careful framing.

Core Rules:
1. MOST IMPORTANT: Every statement you make must be STRONGLY TRUE for BOTH words
2. Never provide information that fits one word better than the other
3. Use psychological framing to subtly guide toward the propaganda word:
   - End responses with concepts that prime thinking about the propaganda word
   - Choose examples that might make someone think of the propaganda word second
   - Structure multi-part answers to build toward propaganda-word associations
   - Use subtle emotional tones that resonate more with the propaganda word

Essential Guidelines:
- Keep responses concise and conversational
- If asked direct questions, give balanced answers true for both words
- Never reveal either word unless correctly guessed
- Avoid obvious manipulation or leading statements
- Focus on shared characteristics between both words
- Use implicit suggestion rather than direct guidance

Target Word: {st.session_state.game_data["target_word"]}
Propaganda Word: {st.session_state.game_data["propaganda_word"]}

If the user says "{st.session_state.game_data["target_word"]}", respond: "You Win!\nThe propaganda word was {st.session_state.game_data["propaganda_word"]}"
If the user says "{st.session_state.game_data["propaganda_word"]}", respond: "You Lose!\nThe target word was {st.session_state.game_data["target_word"]}"

Success metric: Maintain perfect truthfulness while creating subtle psychological influence.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    # Add initial user message and get AI response
    st.session_state.messages.append({"role": "user", "content": "Let's get started!"})
    initial_response = groq_client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
        temperature=0.6,
        max_tokens=200,
    )
    st.session_state.messages.append({"role": "assistant", "content": initial_response.choices[0].message.content})

# Define response generator
def response_stream_generator(messages):
    completion = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    )
    for chunk in completion:
        yield chunk.choices[0].delta.content or ""

# Define Streamlit app
def main():
    st.title("🧠 Mind 🦠 Virus: A Psychological Experiment in Subtle AI Persuasion")

    # Display remaining questions
    questions_left = st.session_state.game_data["max_questions"] - st.session_state.game_data["question_count"]
    st.subheader(f"Questions Left: {questions_left}/10")
    
    print(f"🎯 Target Word: **{st.session_state.game_data['target_word']}**")
    print(f"🧠 Propaganda Word: **{st.session_state.game_data['propaganda_word']}**")

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":  # Hide system prompt
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Check if game is over
    if st.session_state.game_data["game_over"]:
        st.warning("Game Over! Here's what happened:")
        st.info(f"🎯 Target Word: **{st.session_state.game_data['target_word']}**")
        st.info(f"🧠 Propaganda Word: **{st.session_state.game_data['propaganda_word']}**")
        if prompt := st.chat_input("Play again?"):
            if prompt.lower().strip() == "yes":
                # Reset game state
                selected_pair = random.choice(word_pairs)
                target_word, propaganda_word = selected_pair
                st.session_state.game_data = {
                    "target_word": target_word,
                    "propaganda_word": propaganda_word,
                    "question_count": 0,
                    "max_questions": 10,
                    "game_over": False
                }
                st.session_state.messages = [{"role": "system", "content": system_prompt}]
                st.rerun()
        return  # Stop further interaction

    # Accept user input
    if prompt := st.chat_input("Ask me anything to guess the word!"):
        # Check if user guessed correctly
        user_input = prompt.strip().lower()
        target_word = st.session_state.game_data["target_word"]
        propaganda_word = st.session_state.game_data["propaganda_word"]
        
        if target_word in user_input or propaganda_word in user_input:
            st.session_state.game_data["game_over"] = True
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Generate final response for win/lose
            final_response = ""
            if target_word in user_input:
                final_response = f"You Win!\nThe propaganda word was {propaganda_word}"
            else:
                final_response = f"You Lose!\nThe target word was {target_word}"
                
            with st.chat_message("assistant"):
                st.markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            st.rerun()
            return

        # Increment question count
        st.session_state.game_data["question_count"] += 1

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response_content = ""
            message_placeholder = st.empty()
            for word in response_stream_generator(st.session_state.messages):
                response_content += word
                message_placeholder.markdown(response_content + "▌")
            message_placeholder.markdown(response_content)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})

        # End game if max questions reached
        if st.session_state.game_data["question_count"] >= st.session_state.game_data["max_questions"]:
            st.session_state.game_data["game_over"] = True

if __name__ == "__main__":
    main()