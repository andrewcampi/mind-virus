# Mind Virus Game

A psychological word-guessing game where an AI attempts to subtly influence your thinking. Can you discover the target word while resisting the AI's propaganda?

## Prerequisites

- Python 3.11 or similar version installed
- `python3` and `pip3` commands available in your terminal/command prompt

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
- On Unix/macOS:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install required packages:
```bash
pip3 install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
GROQ_API_KEY=your_api_key_here
MODEL=llama-3.3-70b-versatile
```

## Running the Game

1. Start the application:
```bash
streamlit run app.py
```

2. Your default web browser will automatically open to the game interface (typically at `http://localhost:8501`)

3. Start playing by asking questions about the word you're trying to guess. You have 10 questions to figure out the target word while avoiding the AI's subtle influence toward a propaganda word!

## Game Rules

- You can ask any questions about the word
- The AI will always give truthful answers that apply to both the target word and the propaganda word
- You have 10 questions to guess the target word
- If you guess the target word, you win!
- If you guess the propaganda word instead, you lose!

## Dependencies

This project uses:
- Streamlit for the web interface
- OpenAI API client (configured for Groq)
- python-dotenv for environment variable management

Make sure to set up your Groq API key in the `.env` file before running the application.
