## GPT sage in Quantum Odyssey 


### Steps to run the sage:
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

___
Project Organization
------------

    │
    ├── config                                                <- Config files fr differnet elemtnet of the systems
    │   ├── ...                                               <- 
    │   └── gpt.toml                                          <- Exmple of congig file for gpt sage      
    │
    ├── data
    │   ├── enciclopedia                                           <- QO chapter by chapter
    │   ├── request_data                                           <- Data from requests
    │   │    └── history.json                                      <- Dll the Qo info in one file
    │   └── Enciclopedia.txt  
    │
    ├── gpt_sage                                                 <- gpt 
    │   ├── __init__.py                                
    │   ├── assistant.py                                  <- Sage and evaluator 
    │   ├── config.py                                     <- Functions used to load ocnfig file
    │   └── upload_docs.py                                <- FUntions used to upload docs to gpt
    │
    ├── LICENSE                                                
    │
    ├── ReadME.md                                               <- Top level README 
    │   
    ├── example_run_assistant.py                                <- Example of how to run a gpt sage(assistant)
    │   
    ├── requiremetns.txt                                         
    │   
    ├── server.py                                               <-  code used to run a flask server.
    │  
    └── server_test.py                                          <-  code used to sent messages to the server for debugging