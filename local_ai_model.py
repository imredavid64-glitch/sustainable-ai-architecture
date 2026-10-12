import os
import sys
import re
import time
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- SUSTAINABILITY CONSTANTS ---
# Estimates for a MacBook Air + Network + Data Center processing
KWH_PER_SEARCH = 0.0003  # kWh
G_CO2_PER_KWH = 442     # Avg grid carbon intensity (g/kWh)
LITERS_PER_KWH = 1.8    # Water used for cooling/power (L/kWh)

class SustainableAnalyst:
    def __init__(self):
        self.history = []
        self.stop_words = {"what", "is", "the", "how", "to", "of", "in", "on", "for"}

    def calculate_metrics(self, query, raw_data, duration, source_count=0):
        # 1. BIAS ALGORITHM: Checks diversity of sources.
        # High bias if results concentrate on one domain, low bias for variety.
        # No domains == no evidence -> bias is None (undetermined), NOT 1.0.
        domains = re.findall(r'https?://(?:www\.)?([^/]+)', str(raw_data))
        unique_domains = len(set(domains))
        if not domains:
            bias_score = None
        elif len(unique_domains) == 1:
            bias_score = 1.0
        else:
            bias_score = 1.0 - (unique_domains / len(domains))

        # 2. ACCURACY ALGORITHM: Keyword overlap (only if real data returned)
        query_tokens = set(re.findall(r'\w+', query.lower())) - self.stop_words
        data_tokens = set(re.findall(r'\w+', str(raw_data).lower()))
        if not query_tokens or not raw_data or not str(raw_data).strip():
            accuracy = None           # nothing to compare -> undetermined, not 0
        else:
            accuracy = len(query_tokens & data_tokens) / len(query_tokens)

        # 3. SUSTAINABILITY MATH
        emissions = KWH_PER_SEARCH * G_CO2_PER_KWH
        water = KWH_PER_SEARCH * LITERS_PER_KWH

        return {
            "query": query[:15] + "...",
            "sources": source_count,
            "accuracy": accuracy,
            "bias": bias_score,
            "emissions_g": np.round(emissions, 4),
            "water_l": np.round(water, 4),
            "latency_s": np.round(duration, 2)
        }

    def log(self, entry):
        self.history.append(entry)

    def show_dashboard(self):
        if not self.history:
            print("[!] No data yet. Run a few searches first!")
            return
        
        df = pd.DataFrame(self.history)
        print("\n" + "="*40)
        print("  SUSTAINABILITY & BIAS REPORT")
        print("="*40)
        print(df.to_string(index=False))
        print("="*40)

        # Plotting
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Performance Graph (bias may be NaN when no source evidence existed)
        plot_df = df[df['bias'].notna()]
        if not plot_df.empty:
            plot_df.plot(kind='line', x='query', y=['accuracy', 'bias'], ax=ax1, marker='o', colormap='viridis')
            ax1.set_title("Search Quality (Higher Acc / Lower Bias is better)")
        else:
            ax1.set_title("Search Quality (No bias evidence yet)")
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Environment Graph
        df.plot(kind='bar', x='query', y='emissions_g', ax=ax2, color='seagreen', alpha=0.8)
        ax2.set_title("Carbon Footprint per Query (g CO2)")
        
        plt.tight_layout()
        plt.show()

class StandaloneSearchAgent:
    def __init__(self):
        self.analyst = SustainableAnalyst()
        self.stop_words = {"what", "is", "the", "how", "to", "of", "in", "on", "for"}
        print("\n--- STANDALONE AGENT INITIALIZED ---")
        print("[*] Using free, low-energy sources (DuckDuckGo + Wikipedia)")

    def _duckduckgo(self, query, max_results=4):
        """Real web search via the free `ddgs` library (no API key)."""
        try:
            from ddgs import DDGS
        except ImportError:
            return [], "ddgs library not installed"
        try:
            with DDGS(timeout=15) as d:
                results = d.text(query, max_results=max_results)
        except Exception as e:
            return [], f"DDG error: {e}"
        out = []
        for r in results or []:
            href, title, body = r.get("href"), r.get("title"), r.get("body")
            if href and title and body:
                out.append(f"https://{href} | {title} | {body}")
        return out, None

    def _wikipedia(self, query, sentences=2):
        """Free summary source (no API key)."""
        try:
            import wikipedia
        except ImportError:
            return [], "wikipedia library unavailable"
        try:
            wikipedia.set_lang("en")
            titles = wikipedia.search(query, results=1)
            if not titles:
                return [], None
            page = wikipedia.page(titles[0], auto_suggest=False)
            summary = ".".join(page.summary.split(".")[:sentences]) + "."
            out = [f"https://en.wikipedia.org/wiki/{page.title.replace(' ', '_')} "
                   f"| {page.title} | {summary}"]
        except Exception as e:
            return [], f"wikipedia error: {e}"
        return out, None

    async def search_and_think(self, query):
        start_time = time.time()

        # THE ALGORITHM: Query multiple free, low-energy sources and combine.
        print(f"[*] Searching free sources for: {query}...")

        results = []
        notes = []
        for fetch in (self._duckduckgo(query), self._wikipedia(query)):
            out, err = fetch
            results.extend(out)
            if err:
                notes.append(err)

        raw_text = "\n".join(results)
        source_count = len({n.split(" | ")[0] for n in results})

        duration = time.time() - start_time

        # Calculate metrics using the Analyst class
        metrics = self.analyst.calculate_metrics(query, raw_text, duration, source_count)
        self.analyst.log(metrics)

        bias_note = "n/a" if metrics["bias"] is None else f"{metrics['bias']:.2f}"
        acc_note = "n/a" if metrics["accuracy"] is None else f"{metrics['accuracy']:.2f}"
        print(f"[*] sources={source_count} accuracy={acc_note} bias={bias_note} "
              f"emissions={metrics['emissions_g']:.4f} g")

        if not raw_text:
            return "Search complete, but no text summaries were available."
        return raw_text

async def main():
    agent = StandaloneSearchAgent()
    
    print("\nAgent Ready. Enter a question or 'stats' to see the dashboard.")
    
    while True:
        user_input = input("\nYOU: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
        elif user_input.lower() == 'stats':
            agent.analyst.show_dashboard()
            continue
        
        print("Thinking...")
        result = await agent.search_and_think(user_input)
        print(f"\nAI: {result}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess ended by user.")