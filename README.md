# 🤖 Universal AI Dashboard

A powerful, unified Streamlit interface to interact with **ChatGPT (OpenAI)**, **Claude (Anthropic)**, and **Gemini (Google)**. This application features indefinite history tracking using SQL and a template library for rapid prompting.

## ✨ Features

* **Multi-Model Support:** Toggle between GPT-4, Claude 3, and Gemini Pro.
* **Persistent History:** Saves all prompts and responses to a database (Local SQLite or Cloud Postgres).
* **Prompt Library:** 10 pre-configured templates for short tasks and long-form content.
* **Secure:** Integrated with environment variables and Streamlit Secrets.

---

## 🛠️ Local Setup (VS Code)

### 1. Clone and Environment

1. Open **VS Code**.
2. Open the terminal (`Ctrl+` `) and run:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

```


3. Create a virtual environment:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```



### 2. Install Dependencies

```bash
pip install streamlit openai anthropic google-generativeai sqlalchemy

```

### 3. Handling API Keys (Local)

For local development, use a `.env` file or Streamlit's local `secrets.toml`.

**Option A: Using `.env` (Recommended for general Python)**
Create a file named `.env` in the root directory:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

```

**Option B: Using `secrets.toml` (Streamlit Native)**
Create a folder named `.streamlit` and a file inside it called `secrets.toml`:

```toml
OPENAI_API_KEY = "your_key_here"
ANTHROPIC_API_KEY = "your_key_here"
GOOGLE_API_KEY = "your_key_here"

```

---

## ☁️ Deployment & GitHub Secrets

When deploying to the cloud (e.g., Streamlit Community Cloud or Heroku), **never** upload your `.env` or `secrets.toml` files to GitHub.

### 1. Secure your `.gitignore`

Ensure your `.gitignore` file includes:

```text
.env
.streamlit/secrets.toml
chat_history.db
__pycache__/

```

### 2. Configure GitHub Secrets & Variables

To use these keys in a CI/CD pipeline or cloud environment:

1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Add your keys (e.g., Name: `OPENAI_API_KEY`, Value: `sk-...`).

### 3. Streamlit Cloud Deployment

If you are using **Streamlit Community Cloud**:

1. Go to your App Settings on the Streamlit Cloud Dashboard.
2. Locate the **Secrets** section.
3. Paste the contents of your `secrets.toml` directly into the text area.

---

## 🚀 Usage

To launch the app locally:

```bash
streamlit run app.py

```

1. Select your preferred **AI Provider** from the sidebar.
2. Paste your API key (if not already set in secrets).
3. Choose a **Template** to auto-fill the prompt area.
4. View your **Indefinite History** at the bottom of the page.

---

## 🗄️ Database Management

* **Local:** Data is stored in `chat_history.db`.
* **Cloud:** To persist data indefinitely in the cloud, change the `DB_URL` in `app.py` to your hosted PostgreSQL URI provided by services like Supabase or Neon.
