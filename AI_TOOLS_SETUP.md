# AI Tools Setup Guide

## Quick Start Guide for BookShelf AI Tools

This guide will help you set up and use the new AI-powered features in BookShelf.

---

## Prerequisites

- Django project already set up and running
- Python 3.8 or higher
- Internet connection for OpenAI API calls

---

## Installation Steps

### 1. Install Required Packages

Run the following command in your project directory:

```bash
pip install -r requirements.txt
```

This installs:
- `openai>=1.0.0` - OpenAI Python client
- `python-dotenv>=1.0.0` - Environment variable loader

### 2. Get Your OpenAI API Key

1. **Sign up / Log in** to OpenAI:
   - Visit: https://platform.openai.com/signup
   - Create an account or log in with existing credentials

2. **Generate API Key**:
   - Navigate to: https://platform.openai.com/api-keys
   - Click **"Create new secret key"**
   - Give it a name (e.g., "BookShelf AI Tools")
   - Copy the key (starts with `sk-...`)
   - **Important**: Save it securely - you won't be able to see it again!

3. **Check Billing** (if needed):
   - Go to: https://platform.openai.com/account/billing
   - Add payment method if required
   - Note: GPT-3.5-turbo is very affordable (typically $0.001-0.002 per request)

### 3. Create `.env` File

**On Windows (PowerShell):**
```powershell
cd "C:\Users\User\Desktop\cs50web finall"
New-Item -Path .env -ItemType File
notepad .env
```

**On macOS/Linux:**
```bash
cd ~/path/to/project
touch .env
nano .env
```

### 4. Add Your API Key to `.env`

Paste the following into your `.env` file:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Replace `sk-your-actual-api-key-here` with your actual OpenAI API key.

**Save and close the file.**

### 5. Add `.env` to `.gitignore` (Important!)

Create or edit `.gitignore` in your project root:

```gitignore
# Environment variables
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
db.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### 6. Restart Django Server

Stop your Django server (Ctrl+C) and restart it:

```bash
python manage.py runserver
```

The server needs to restart to load the environment variables from `.env`.

---

## Using AI Tools

### Accessing the AI Tools Page

1. **Log in** to your BookShelf account
2. Click **"AI Tools"** in the navigation bar
3. Or navigate to: `http://127.0.0.1:8000/ai/`

### Feature 1: AI Book Summarizer

**What it does**: Summarizes any text passage into concise, clear summaries.

**How to use**:
1. Click **"Try Now"** on the AI Book Summarizer card
2. Paste text into the textarea (book excerpts, articles, etc.)
3. Click **"Generate Summary"**
4. Wait 2-5 seconds for AI processing
5. View your summary in the result box

**Example Input**:
> "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair..."

### Feature 2: AI Book Recommender

**What it does**: Recommends 3-5 books based on your interests.

**How to use**:
1. Click **"Try Now"** on the AI Book Recommender card
2. Enter a topic or genre (e.g., "space exploration", "historical fiction", "productivity")
3. Click **"Get Recommendations"**
4. Wait for AI to generate suggestions
5. Browse recommended books with authors and descriptions

**Example Topics**:
- "psychological thrillers"
- "artificial intelligence ethics"
- "ancient Roman history"
- "mindfulness and meditation"

### Feature 3: AI Quiz Generator

**What it does**: Creates 5 quiz questions about any book to test your knowledge.

**How to use**:
1. Click **"Try Now"** on the AI Quiz Generator card
2. Enter book title (e.g., "1984")
3. Enter author name (e.g., "George Orwell")
4. Select difficulty: Beginner, Intermediate, or Advanced
5. Click **"Generate Quiz"**
6. Review 5 questions with answers

**Example**:
- **Title**: "The Great Gatsby"
- **Author**: "F. Scott Fitzgerald"
- **Difficulty**: Intermediate

---

## Troubleshooting

### Error: "OpenAI API key not configured"

**Solution**: 
- Ensure `.env` file exists in project root
- Verify the file contains: `OPENAI_API_KEY=sk-...`
- Restart Django server after creating `.env`

### Error: "Invalid API key"

**Solution**:
- Check that you copied the entire API key (starts with `sk-`)
- Verify key is still active at https://platform.openai.com/api-keys
- Ensure no extra spaces or quotes around the key in `.env`

### Error: Rate limit exceeded

**Solution**:
- OpenAI has rate limits based on your plan
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan if needed

### AI returns incomplete or weird responses

**Solution**:
- This is normal occasionally - AI responses can vary
- Try submitting the request again
- Adjust your input to be more specific or clear

### Modals not opening

**Solution**:
- Check browser console for JavaScript errors (F12)
- Ensure you're logged in (AI Tools requires authentication)
- Clear browser cache and reload

---

## Cost Estimates

OpenAI API pricing for GPT-3.5-turbo (as of 2024):

- **Input**: ~$0.50 per 1M tokens
- **Output**: ~$1.50 per 1M tokens

**Typical request costs**:
- Summarizer: ~$0.001-0.002 per request
- Recommender: ~$0.002-0.003 per request
- Quiz Generator: ~$0.002-0.004 per request

**Monthly estimate**: 100 requests ≈ $0.20-0.40

💡 **Tip**: Monitor usage at https://platform.openai.com/usage

---

## Security Best Practices

✅ **DO**:
- Keep your API key in `.env` file only
- Add `.env` to `.gitignore`
- Never commit API keys to Git
- Rotate keys if accidentally exposed
- Monitor API usage regularly

❌ **DON'T**:
- Share your API key with others
- Commit `.env` to version control
- Expose API key in frontend JavaScript
- Use the same key for multiple projects (optional, but good practice)

---

## Customization

### Change AI Model

Edit `library/views.py` in the OpenAI API calls:

```python
# For better quality (more expensive)
model="gpt-4"

# Current default (cost-effective)
model="gpt-3.5-turbo"

# For even cheaper (lower quality)
model="gpt-3.5-turbo-0125"
```

### Adjust Response Length

Modify `max_tokens` parameter:

```python
max_tokens=150   # Shorter responses
max_tokens=500   # Medium length
max_tokens=1000  # Longer responses
```

### Customize System Prompts

Edit the `system` role content in API calls:

```python
{
    "role": "system",
    "content": "You are a literary expert specializing in classic novels..."
}
```

---

## Getting Help

- **OpenAI Documentation**: https://platform.openai.com/docs
- **OpenAI Status**: https://status.openai.com
- **Django Documentation**: https://docs.djangoproject.com

---

## Features Coming Soon 🚀

1. **Chat with Your Book**: Interactive AI conversations about your books
2. **AI Progress Predictor**: Estimate reading completion times based on your habits

---

**Happy Reading with AI! 📚🤖**

---

*Last Updated: October 2025*
*BookShelf AI Tools v1.0*

