# 🌱 Sustainable Search Agent & Analyst

Welcome to the **Sustainable Search Agent**, a lightweight Python tool that acts as your eco-conscious research assistant. Not only does it fetch real-time information from free web sources (DuckDuckGo and Wikipedia) without needing API keys, but it also tracks the environmental footprint (carbon emissions and water usage) of every single search you make!

---

## 🧭 Architecture Explained (In a Non-Technical Way)

Imagine you have a smart, eco-conscious research assistant working at a desk:

1. **The Researcher (`StandaloneSearchAgent`):** 
   When you ask a question, this part of the system runs out to public libraries and news stands (DuckDuckGo and Wikipedia) to quickly gather relevant summaries and bring them back to you.

2. **The Environmental Bookkeeper (`SustainableAnalyst`):** 
   Right beside the researcher sits an accountant who measures the invisible cost of your question. Every time a search runs, this bookkeeper calculates how much electricity your device and the data centers used, translating it into grams of carbon dioxide ($\text{CO}_2$) and milliliters of water consumed.

3. **The Quality Control Inspector:** 
   The bookkeeper also checks the homework. It looks at the sources used to see if they are diverse (making sure you aren't getting a biased, one-sided view) and checks if the answers actually match what you asked (accuracy).

4. **The Journal / Dashboard:** 
   At any time, you can ask to see your search history. The system pulls out a visual ledger with charts showing your carbon footprint trends and search quality over time.

---

## ✨ Key Features

- **Zero API Keys Required:** Uses open-source libraries (`duckduckgo_search` and `wikipedia`) to fetch live data.
- **Environmental Tracking:** Estimates carbon emissions ($\text{g }\text{CO}_2$) and water usage ($L$) per search based on standard data center and network metrics.
- **Quality & Bias Metrics:** Automatically scores search result diversity (bias) and keyword relevance (accuracy).
- **Interactive Dashboard:** Generates visual graphs using `matplotlib` to display your search performance and environmental impact side by side.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed along with the required libraries:
```bash
pip install pandas numpy matplotlib ddgs wikipedia
```

### Running the Agent
Run the script from your terminal:
```bash
python local_ai_model.py
```

- Type your question to perform a search.
- Type `stats` to view your sustainability and quality dashboard.
- Type `exit` or `quit` to close the session.