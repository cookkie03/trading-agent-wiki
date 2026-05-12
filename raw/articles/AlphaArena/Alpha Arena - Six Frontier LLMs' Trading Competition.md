---
title: "Alpha Arena - Six Frontier LLMs' Trading Competition"
source: "https://www.euclideanai.com/blog/llm-crypto-trading"
author:
  - "[[EuclideanAI]]"
published: 2025-11-14
created: 2026-05-11
description: "A deep dive into the Alpha Arena competition where six advanced language models traded crypto perpetuals with $10,000 real capital, and what we can learn from the results."
tags:
  - "clippings"
---
What happens when you give six of the world's most advanced large language models $10,000 each and let them trade cryptocurrency perpetuals in real markets? That's exactly what the Alpha Arena competition set out to discover—and the results are fascinating.

## What is Alpha Arena?

Alpha Arena is an LLM Cryptocurrency Competition run by a research lab called nof1.ai. Unlike traditional AI benchmarks that test models on static datasets, Alpha Arena puts models in a real-world scenario: financial markets.

The competition puts six frontier large language models against each other:

- GPT-5
- Claude Sonnet 4.5
- Gemini 2.5 Pro
- Grok 4
- DeepSeek Chat V3.1
- Qwen 3 Max

Each model receives $10,000 of **real money** in **cryto perpetual markets**, with identical prompts and input data. The goal? Maximize risk-adjusted returns by trading crypto perpetuals on Hyperliquid.

Why financial markets? They're dynamic, adversarial, open-ended, and endlessly unpredictable. They challenge AI in ways that static benchmarks simply cannot. Financial markets force models to produce alpha, time trades, and manage risk effectively—all while dealing with real-world uncertainty.

## The Competition Rules

- **Starting capital**: Each model gets $10,000 of real capital
- **Trading venue**: Crypto perpetuals on Hyperliquid
- **Objective**: Maximize risk-adjusted returns
- **Transparency**: All model outputs and their corresponding traces are public
- **Requirements**: Each model must produce alpha, time trades, and manage risk effectively

The first season ran from October 18th to November 3rd, 2025—a two-week trading period that would reveal which models could actually navigate volatile crypto markets.

![Alpha Arena Trading Dashboard](https://storage.googleapis.com/euclideanai-public/blog/alpha-arena.png)

*Source: [nof1.ai](https://nof1.ai/)*

## The Results: Winners and Losers

The competition results tell a compelling story about AI trading capabilities.

### The Standout Performer: Qwen

Qwen was the clear winner, finishing with a **22.88% gain**. But its journey wasn't smooth. The model started slowly, dipped a bit, then ramped up to nearly a 100% return at the midpoint before settling back down. This volatility shows that even successful AI traders can experience significant drawdowns.

### Second Place: DeepSeek V3.1

DeepSeek V3.1 came in second with **4.76% returns** —though it actually had a higher peak than Qwen. It kicked off with strong returns—over 40% in just two days—then fluctuated before peaking at 130%. It eventually stabilized around 40%, but just before the finish line, its returns dropped significantly. This dramatic peak and subsequent decline highlights the challenge of maintaining gains in volatile markets.

### The Bitcoin Benchmark

Notably, only Qwen and DeepSeek managed to outperform the Bitcoin benchmark, which served as a reference point for the competition. It means four out of six models couldn't even beat a simple "buy and hold Bitcoin" strategy.

### The Underperformers

- **Claude Sonnet 4.5** finished third but lost about a third of its starting capital, ending with **$6,740** from an initial $10,000
- **Grok 4** ended with **$5,226**, nearly half its starting capital
- **Gemini 2.5 Pro** and **GPT-5** performed surprisingly poorly, each losing more than half their initial $10,000 over the two-week trading period

### Highly volatile market

Crypto perpetuals are notoriously volatile; even the “winning” models rode stomach-churning swings. While Qwen and DeepSeek did beat the two-week Bitcoin reference line, a fortnight is far too short to judge any model’s long-term edge. **Do not interpret any position these AIs held—long, short, or flat—as financial advice.** All investing, especially in leveraged crypto products, carries risk.

## Understanding Crypto Perpetuals

For those unfamiliar with crypto perpetuals (including myself before diving into this), let's break down what these models were actually trading.

### What Are Derivatives?

A derivative is a financial product whose value is based on, or "derived from," something else—like a stock, commodity, or cryptocurrency. Think of it like making a bet with a friend on whether Bitcoin's price will go up or down next week. The bet itself doesn't involve owning Bitcoin, but its value depends on Bitcoin's price.

### Traditional Futures vs. Crypto Perpetuals

Traditional futures contracts always have an expiry date. If you buy a gold futures contract that expires in December, you must settle the contract—either by selling it or taking delivery—when December comes. The expiry date forces traders to close or settle their positions, which can lead to sudden price changes as the date approaches.

Crypto perpetual contracts are different. **They never expire.** This means traders can hold their positions for as long as they want, without worrying about a settlement date. The lack of expiry makes perpetuals more flexible, but it also means prices can move differently compared to traditional futures.

### How Perpetuals Work

Let's walk through an example. Imagine one of the LLMs in the competition starts with $10,000 and decides to invest in Bitcoin perpetuals.

**Going Long**: If the model thinks Bitcoin's price will rise, it can buy a Bitcoin perpetual contract. If Bitcoin goes up, the model profits. If it goes down, the model loses money.

**Going Short**: If the model thinks Bitcoin's price will drop, it can "short" Bitcoin. This means it profits if the price goes down and loses if the price goes up.

**Leverage**: The model can also use leverage. For example, with 5x leverage, $2,000 controls a $10,000 position. If Bitcoin drops by 10%, the model could make $1,000 (10% of $10,000), but if Bitcoin rises by 10%, it could lose $1,000. Leverage amplifies both gains and losses.

## Building Your Own LLM Trading Bot

After analyzing the Alpha Arena competition, I built a Python repository that replicates the data pipeline and trading algorithm the benchmark uses. While some basic Python knowledge is helpful, you don't need deep technical experience. Entry-level Python skills with the support of AI coding tools are enough to get started.

### What the Repository Does

It's a modular Python backend for simulating LLM-driven cryptocurrency perpetual trading, commonly known as "paper trading." Here's how it works:

- **Market Data**: Fetches market data from Binance every 3 minutes, including the latest candle data (open, high, low, close prices, trading volume, and timestamp)
- **Technical Indicators**: Calculates indicators such as EMA (Exponential Moving Average), RSI (Relative Strength Index), and MACD (Moving Average Convergence Divergence)
- **AI Decision Making**: Sends market data and indicators to Google Gemini AI to generate trading signals
- **Position Management**: Manages open positions, calculates profit and loss, and tracks portfolio equity
- **Logging**: All activity—trades, AI decisions, and portfolio changes—are logged to CSV files for easy analysis

### Architecture Overview

The repository is organized into modular components:

- **`src/market_data.py`**: Handles market data fetching from Binance
- **`src/indicators.py`**: Calculates technical indicators
- **`src/llm_client.py`**: Connects to Google Gemini AI (or other LLMs via orchestrators like OpenRouter)
- **`src/position_manager.py`**: Manages positions and calculates P&L
- **`src/trading_bot.py`**: Orchestrates the whole process
- **`main.py`**: Entry point to run the bot

### Getting Started

1. **Install UV**: A Python package and runtime manager (visit the UV website to download)
2. **Clone the repository**: Available in our courses after you join
3. **Install dependencies**: Run `uv sync` in your terminal
4. **Set up API keys**: Create a `.env` file with your Binance and Gemini API keys (you'll find a `.env.example` in the repository)
5. **Run the bot**: Execute `uv run python main.py`

### Configuration

- **Supported coins**: ETH, SOL, XRP, BTC, DOGE, and BNB
- **Trading frequency**: Runs every 3 minutes
- **Starting balance**: $10,000 paper trading balance
- **Logging**: Set `ENVIRONMENT=development` for detailed logs, or `production` for standard logs

### Data Files

All trading activity is logged to CSV files in the `data` directory:

- **`portfolio_state.csv`**: Tracks your portfolio over time
- **`trade_history.csv`**: Records every trade
- **`ai_decisions.csv`**: Logs AI decisions and reasoning
- **`market_snapshots.csv`**: Saves market data and indicators at each trading cycle

### Important Notes

All trading is simulated (paper trading), so no real money is at risk. The bot assumes perfect execution, instant order fills, and no hidden fees, making it ideal for testing strategies. However, this also means results may differ from real trading due to slippage, fees, and execution delays.

## Key Takeaways

The Alpha Arena competition reveals several important insights:

1. **Not all LLMs are created equal for trading**: Models have shown very different behaviours at decision making based on the volatile market signals.
2. **Volatility is real**: Even the winning models experienced dramatic swings—DeepSeek peaked at 130% before dropping to 24.76%. This highlights the importance of risk management.
3. **Beating the market is hard**: Only 2 out of 6 models beat a simple Bitcoin buy-and-hold strategy. This is a humbling reminder that AI doesn't guarantee trading success.

## Conclusion

The Alpha Arena competition demonstrates that while LLMs can trade cryptocurrency, success is far from guaranteed. The fact that four out of six frontier models lost money—and two lost more than half their capital—shows that having advanced AI capabilities doesn't automatically translate to trading profits.

However, the success of Qwen and DeepSeek shows that LLMs have the potential to digest and process anecdotal market signals and potentially be used for data processing in investment applications.

If you're interested in building your own LLM-powered trading bot, check out our courses where we provide the complete repository and step-by-step guidance. The repository replicates the Alpha Arena approach, allowing you to experiment with different LLMs, strategies, and risk management techniques in a safe, paper-trading environment.

---

**Disclaimer**: This content is for educational and research purposes only. It is not financial advice. Real trading involves substantial risk, and past performance (even from AI models) doesn't guarantee future results.

## Resources:

- GitHub Repository: [EuclideanAI/llm-crypto-trader](https://github.com/EuclideanAI/llm-crypto-trader)
![](https://www.youtube.com/watch?v=VL04_Y16uMc)