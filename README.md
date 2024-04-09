## Getting started

### Local usage
1. Clone this repository
2. Create an virtual env and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install requirements to run the examples 
```bash
pip install -r requirements.txt
```
4. Add OpenAI  token :
```bash
export OPENAI_API_KEY="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"
```

5. Run server :
```bash
gunicorn -w 4 -b 0.0.0.0:800 server:app
```