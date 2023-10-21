# rag-chatgpt
A repo to work on RAG for personal understanding

Setup python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Download spacy model
```bash
python -m spacy download en_core_web_sm
```

Export OpenAI key
```bash
export OPENAI_API_KEY="sk-P..."
```

Download a video text
```bash
python ./video-reader.py tesla '5b9H-JiS5J4'
```

Summarize the text
```bash
python ./openai_text_summary.py tesla
```

Starting Verba
```bash
verba start --model "gpt-3.5-turbo"
```

Importing into Verba
```bash
verba import --path tesla --model "gpt-3.5-turbo" --clear True
```
