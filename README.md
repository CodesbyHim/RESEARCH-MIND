# ResearchMind

An AI-powered multi-agent research assistant that automates web research and generates structured research reports using Python, LangChain, Google Gemini, and Tavily.

## Overview

ResearchMind is designed to simplify the research process by coordinating multiple specialized AI agents. Instead of relying on a single AI prompt, the application follows a sequential workflow in which each agent performs a specific task.

The system searches for relevant information, extracts useful content from webpages, generates a structured report, and evaluates the report through a critic agent.

## Features

- **Automated Web Search:** Finds relevant web resources using Tavily Search.
- **Webpage Content Extraction:** Extracts readable content from webpages using BeautifulSoup.
- **Multi-Agent Workflow:** Coordinates specialized agents for different research tasks.
- **AI-Generated Reports:** Produces structured research reports based on gathered information.
- **Report Evaluation:** Uses a critic agent to review the generated report and provide feedback.
- **Interactive Streamlit Interface:** Provides a simple interface to enter research topics and view results.
- **Report Download:** Allows users to download the generated research report in Markdown format.

## Multi-Agent Architecture

ResearchMind follows a sequential four-stage research pipeline:

1. **Search Agent**
   - Searches the web for relevant resources.
   - Collects titles, URLs, and search snippets.

2. **Reader Agent**
   - Processes the discovered URLs.
   - Extracts and summarizes relevant webpage content.

3. **Writer Agent**
   - Uses the collected research material.
   - Generates a structured research report.

4. **Critic Agent**
   - Evaluates the generated report.
   - Provides feedback on its quality and completeness.

### Workflow

Research Topic → Search Agent → Reader Agent → Writer Agent → Critic Agent → Final Research Output

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| LangChain | Agent creation and orchestration |
| Google Gemini | Large language model |
| Tavily Search | Web search |
| BeautifulSoup | Webpage content extraction |
| Requests | HTTP requests |
| Streamlit | Interactive web application |
| python-dotenv | Environment variable management |

## Project Structure

```text
ResearchMind/
│
├── app.py              # Streamlit application
├── agents.py           # AI agent definitions
├── pipeline.py         # Multi-agent research pipeline
├── tools.py            # Web search and scraping tools
│
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <https://github.com/CodesbyHim/RESEARCH-MIND.git>
cd ResearchMind
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep your `.env` file private. Never commit API keys or other credentials to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access ResearchMind.

## Usage

1. Launch the Streamlit application.
2. Enter a topic you want to research.
3. Start the research process.
4. Follow the progress of the four research stages.
5. Review the generated report and critic feedback.
6. Download the report in Markdown format.

## Current Status

The initial implementation of ResearchMind is complete, including the multi-agent research pipeline and Streamlit interface.

The project is open to further improvements and experimentation.

## Future Improvements

- Improve source verification and citation handling.
- Add more robust error handling and retry mechanisms.
- Improve research quality through iterative agent collaboration.
- Support exporting reports to PDF and DOCX.
- Add research history and persistent storage.
- Explore additional LLM providers and model configurations.

## License

This project is licensed under the MIT License.
