# LaunchLens 🚀

LaunchLens is an AI-powered startup research assistant that helps founders evaluate product opportunities by combining demand signals and supply signals.

## Problem

Founders often make product decisions with incomplete information.

* Demand data exists on search engines and trend platforms.
* Supply data exists on marketplaces and customer reviews.
* These sources are rarely analyzed together.

LaunchLens aims to bridge that gap.

## Features

* Conversational research assistant
* FastAPI backend
* Gradio frontend
* LLM-powered insights
* Conversation memory (sliding window)
* Modular agent architecture

## Architecture

```text
Gradio UI
    |
FastAPI API
    |
Chat Agent
    |
LLM Provider
```

## Project Structure

```text
LaunchLens/
│
├── run.py
├── requirements.txt
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── config/
│   ├── memory/
│   ├── prompts/
│   └── ui/
```

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```text
NVIDIA_API_KEY=your_api_key
```

## Run

Start the application:

```bash
python run.py
```

UI:

```text
http://localhost:7890
```

API:

```text
http://localhost:8000/docs
```

## Roadmap

* Web search integration
* Amazon product analysis
* Pricing intelligence
* RAG knowledge base
* Multi-user sessions
* Deployment
