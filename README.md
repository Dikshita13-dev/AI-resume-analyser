# 📄 AI Resume Analyzer

An AI-powered web app that compares your resume against a job description and gives you an instant match score, skill gap breakdown, and concrete suggestions to improve your resume — powered by Groq's free LLM API.

## Features

- Upload your resume as PDF, DOCX, or TXT
- Paste in any job description
- Get an AI-generated match score (0–100)
- See matched skills vs. missing skills
- Get a breakdown of your strengths and gaps
- Receive concrete, actionable suggestions to improve your resume for that specific role

## Tech Stack

- **Frontend/UI:** Streamlit
- **Text extraction:** pdfplumber (PDF), python-docx (DOCX)
- **AI analysis:** Groq API running `openai/gpt-oss-120b`
- **Language:** Python

## How It Works

1. The app extracts raw text from your uploaded resume file
2. That text, along with the job description, is sent to an LLM via the Groq API with a structured prompt
3. The model returns a JSON response containing the match score, matched/missing skills, strengths, gaps, and improvement suggestions
4. Streamlit renders the results in a clean, readable layout

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key

Sign up at [console.groq.com/keys](https://console.groq.com/keys) — no credit card required.

### 4. Set your API key as an environment variable

```bash
export GROQ_API_KEY="your-key-here"   # macOS/Linux
set GROQ_API_KEY="your-key-here"      # Windows (cmd)
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Usage

1. Upload your resume (PDF, DOCX, or TXT)
2. Paste the job description into the text box
3. Click **Analyze Match**
4. Review your match score, skill gaps, and suggestions

## Running in Google Colab

A Colab notebook version is included that runs the same Streamlit app inside Colab and exposes it via a public URL using `localtunnel` — no local installation required. See `AI_Resume_Analyzer_Streamlit_Colab.ipynb`.

## Notes

- Your API key is never hardcoded or stored — it's read from an environment variable at runtime.
- The Groq free tier is sufficient for personal projects and demos (rate-limited, no cost).
- Model used: `openai/gpt-oss-120b` (Groq's recommended replacement for the deprecated Llama 3.3 70B).

## Possible Extensions

- Support uploading multiple resumes and rank them against one job description
- Cache analysis results to avoid repeated API calls
- Add a classic NLP fallback (spaCy + embeddings) for offline/no-API-cost matching
- Deploy on Streamlit Community Cloud for a permanent public link

## License

MIT
