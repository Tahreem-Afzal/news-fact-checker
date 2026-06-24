# AI-News-Fact-Checking-and-Summarization-Chatbot

## Setup & Run in VS Code

### Step 1 — Open the project
1. Open VS Code  
2. Go to File → Open Folder → select the `news_chatbot` folder  

### Step 2 — Create a virtual environment
Open the VS Code terminal (Ctrl + `) and run:
```
python -m venv venv
```

### Step 3 — Activate the virtual environment
Windows:
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```

### Step 4 — Install dependencies
```
pip install -r requirements.txt
```


### Step 5 — Add your API key
1. Copy `.env.example` to a new file named `.env`  
2. Open `.env` and replace `your_api_key_here` with your actual API key  
   (Anthropic or Grok depending on what you are using)

### Step 6 — Run the app
```
python app.py
```

### Step 7 — Open in browser
Go to: http://localhost:5000

---
Project structure:
```
news_chatbot/
├── app.py              ← Flask backend (API routes)
├── requirements.txt    ← Python dependencies
├── .env                ← Your API key (never share this)
├── .env.example        ← Template for .env
└── static/
    └── index.html      ← Frontend chatbot UI
```
