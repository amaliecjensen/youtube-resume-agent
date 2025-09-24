# YouTube Transcript Agent

En AI-drevet agent der kan generere resuméer af YouTube videoer ved hjælp af OpenAI's GPT modeller.

## Funktioner

- Henter transkripter fra YouTube videoer
- Genererer resuméer og besvarelses ved hjælp af AI
- Interaktiv chat-interface til at stille spørgsmål om videoindhold

## Setup

1. Klon repository:
```bash
git clone https://github.com/amaliecjensen/youtube-resume-agent.git
cd youtube-resume-agent
```

2. Installer dependencies:
```bash
pip install -r requirements.txt
```

3. Opret en `.env` fil med din OpenAI API nøgle:
```
OPENAI_API_KEY=din_api_nøgle_her
```

4. Kør scriptet:
```bash
python script.py
```

## Brug

Start programmet og indtast spørgsmål om YouTube videoer. Programmet vil bruge AI til at give svar baseret på videoens indhold.

## Teknologier

- Python
- LangChain
- OpenAI GPT
- python-dotenv

## Status

🚧 **Under udvikling** - Dette projekt er stadig under udvikling og flere funktioner vil blive tilføjet.