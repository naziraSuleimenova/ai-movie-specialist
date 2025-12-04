# Movie Assistant Agent

A conversational AI agent that answers questions and fetches movie info from OMDB API. Includes automatic conversation summarization when token limit is exceeded.

## Setup

Create a `.env` file:
```
OPENAI_API_KEY=your_openai_key
OMDB_API_KEY=your_omdb_key
```

Install and run:
```bash
python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
pip install -r requirements.txt
python agent.py
```

## Example
```
You: What's the plot of Inception?
[Calling tool: get_movie_plot]
Assistant: A thief who steals corporate secrets through dream-sharing technology is offered a chance to erase his criminal record by planting an idea into a target's subconscious.

You: Who directed it?
[Calling tool: get_movie_information]
Assistant: Christopher Nolan.

You: What's 2 + 2?
Assistant: 4
```