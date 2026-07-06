# LaunchLens 🚀

LaunchLens is an AI-powered startup research assistant that helps founders evaluate product opportunities by combining demand signals and supply signals.

## Problem

Founders often make product decisions with incomplete information.

- Demand data exists on search engines and trend platforms.
- Supply data exists on marketplaces and customer reviews.
- These sources are rarely analyzed together.

LaunchLens aims to bridge that gap.

## Overview

LaunchLens takes a product idea in plain language and turns it into a research-backed verdict.

It helps answer questions like:

- Is there enough demand for this idea?
- How crowded is the market?
- What are people already buying or searching for?
- What would make this idea stand out?

The goal is to help founders move from intuition to evidence before they pitch or build.

## How Research Works

LaunchLens performs research in stages:

1. The user enters a product idea.
2. The assistant extracts the core product, audience, market, and constraints.
3. It generates search terms for demand research and competitor research.
4. It searches relevant sources for similar products, trends, pricing, and customer feedback.
5. It combines the results into a clear conclusion.

## Sources Referred

LaunchLens uses multiple source types to build a balanced view of the market.

### Demand signals
- Search engines
- Trend platforms
- Blog posts
- YouTube videos
- Community discussions

### Supply signals
- Marketplaces
- Product listings
- Customer reviews
- Pricing pages
- Competitor websites

This helps the assistant compare what people want with what is already available.

## How the Conclusion Is Made

The final verdict is based on three things:

- Demand strength: whether the idea has clear interest or search activity.
- Supply intensity: whether the market already has many similar products.
- Differentiation gap: whether there is still room to stand out.

The assistant then gives a verdict such as:

- Pitchable
- Needs refinement
- High competition
- Weak demand

It also explains why the idea received that verdict.

## Features

- Conversational research assistant
- FastAPI backend
- Gradio frontend
- LLM-powered insights
- Conversation memory
- Modular agent architecture

## Tech Stack

- Python
- FastAPI
- Gradio
- NVIDIA API / LLM provider
- Python dotenv for environment variables
- Requests / HTTP utilities for external calls
- Memory module for conversation context

## Graph Image

Add your architecture diagram here.

![LaunchLens Architecture](assets/graph.png)

## Folder Structure

```text
LaunchLens/
├── run.py
├── requirements.txt
├── README.md
├── .env
├── assets/
│   └── graph.png
└── app/
    ├── agents/
    ├── api/
    ├── config/
    ├── graphs/
    │   └── nodes/
    ├── memory/
    ├── prompts/
    ├── services/
    ├── ui/
    └── utils
```

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows
```bash
venv\Scripts\activate
```

### macOS / Linux
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```text
NVIDIA_API_KEY=<key>
SERP_API_KEY=<key>
OXYLABS_API_UN=<un>
OXYLABS_API_PW=<pw>
```

Add any other keys required by your setup.

## How to Run

Start the application:

```bash
python run.py
```

### UI
The Gradio UI will be available at:

```text
http://localhost:5001
```

### API
The FastAPI documentation will be available at:

```text
http://localhost:8000
```

