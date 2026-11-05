# MonteCarloSimulation
Predicts the probability of an up move for any ticker (stocks, crypto, futures, forex...) with an XGBoost model on 23 technical features, then runs Monte Carlo simulations to estimate likely price ranges. Walk-forward validated. Research tool, not financial advice.


1. Load real price data from Yahoo Finance or CSV
2. Engineers 23 technical features regarding price
3. Trains an XGBoost classifier to estimate P(price up) over a chosen horizon, validated with walk-forward splits
4. Runs Monte Carlo simulations two ways; pure historical bootstrap, biased by model's current prediction. Provides a probability distribution of where price could land

# Start

## Step 1: Python Check (3.10 or newer)
python --version

## Step 2: Install dependencies
python -m venv .venv

#### Windows:
.venv\Scripts\activate
#### macOS / Linux:
source .venv/bin/activate

#### Install all dependencies via file
pip install -r requirements.txt
