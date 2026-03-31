#  AEIDSS — AI-Powered Epidemic Intelligence & Decision Support System

<div align="center">

![AEIDSS Banner](https://img.shields.io/badge/AEIDSS-Epidemic%20Intelligence-1d6fdb?style=for-the-badge&logo=activity&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES2020-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4.1-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A fully interactive, browser-based epidemic intelligence dashboard built on the Johns Hopkins COVID-19 CSSE dataset. Features real-time anomaly detection, time-series forecasting with confidence intervals, risk classification for 201 countries, intervention simulation, and universal AI analysis support across 8+ AI providers — all running locally with zero cloud dependency.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation--setup) • [Tech Stack](#-tech-stack--tools) • [Workflow](#-technical-workflow) • [API Setup](#-ai-analysis-setup)

</div>

---

## 📋 Project Overview

AEIDSS (AI-Powered Epidemic Intelligence & Decision Support System) is a hackathon project that transforms raw COVID-19 time-series data into actionable epidemic intelligence. The system provides:

- **Predictive modeling** of disease spread using statistical forecasting algorithms
- **Risk classification** of all 201 tracked countries using a composite scoring model
- **Early warning detection** using rolling Z-score anomaly detection across the full dataset
- **Intervention simulation** using a modified SEIR model with 5 adjustable parameters
- **Interactive visualizations** with 15+ chart types across 5 analytical tabs
- **AI-powered analysis** compatible with 8+ AI providers (Groq, Gemini, OpenAI, etc.)

### Dataset
| Property | Value |
|----------|-------|
| Source | Johns Hopkins University CSSE |
| Coverage | 201 countries & territories |
| Time Range | January 22, 2020 — March 9, 2023 |
| Data Points | 163,000+ observations |
| Sub-regional Data | 8 countries (Australia, Canada, China, France, UK, Netherlands, Denmark, New Zealand) |
| Global Confirmed | 676.4 million cases |
| Global Deaths | 6.88 million |
| Global CFR | ~1.02% |

---

## ✨ Features

###  Tab 1 — Overview
- **Dual-axis timeline** — Confirmed cases (left axis) + Deaths (right axis) on one chart
- **Regional doughnut chart** — Cases broken down by world region (Europe, Asia, Americas, Africa, Oceania)
- **Top-15 grouped bar chart** — Logarithmic scale comparison of cases vs deaths
- **Bubble chart** — CFR% × Total Cases × Deaths (3 dimensions simultaneously)

### Tab 2 — Time-Series Forecasting
- **3 selectable forecasting models:**
  - **Holt Double Exponential Smoothing (DES)** — captures level + trend components
  - **Exponential Moving Average (EMA)** — weighted smoothing with configurable α
  - **Linear OLS Regression** — ordinary least squares with prediction intervals
- **95% Confidence Interval bands** — uncertainty widens correctly over time
- **Model diagnostics** — RMSE, R² goodness-of-fit, residuals chart with ±1σ bands
- **Configurable horizon** — 30, 60, 90, or 180 days
- **New cases trend chart** — raw bars + EMA overlay (α = 0.3)

### Tab 3 — Risk Assessment
- **201-country risk table** — searchable, filterable, with sub-region tags
- **Composite risk scoring** — formula: `growth_rate × 0.5 + CFR × 5 + weekly_cases_factor`
- **SHAP feature importance** — explains which factors drive risk classification
- **Radar/spider chart** — multi-dimension comparison of top 5 highest-risk countries
- **Full CFR bar chart** — all 201 countries sorted, colour-coded by severity

### 🚨 Tab 4 — Early Warning System
- **Live Z-score anomaly detection** scans all 201 countries in real-time
- **Configurable threshold** — Sensitive (Z≥2.0) / Standard (Z≥2.5) / Strict (Z≥3.0) / Critical (Z≥4.0)
- **Configurable rolling window** — 4, 8, or 12 periods
- **Z-score timeline** — colour-segmented line chart per country (red/orange/blue by severity)
- **Peak Z-score ranking** — horizontal bar chart of top 20 worst historical surges
- **Raw vs EMA chart** — new cases bars + smoothed trend overlay

### Tab 5 — Intervention Simulation
- **Modified SEIR model** with 5 adjustable sliders:
  - Mobility Reduction (0–100%)
  - Vaccination Rate (0–100%)
  - Mask Compliance (0–100%)
  - Testing Rate (0–1000 per 100K)
  - Forecast Days (7–180)
- **R-effective calculation** — `R_eff = R₀ × (1−mobility×0.5) × (1−vaccination×0.8) × (1−masks×0.3)`
- **What-if projection** — baseline vs intervention dual-area chart
- **Output metrics** — Cases Averted, Deaths Averted, Reduction %

### Universal AI Analysis (Optional)
- Works with **8+ AI providers** — auto-detects provider from key format
- Analysis types: Risk Assessment, Key Drivers, Intervention Advice, Forecast, Sub-region Analysis
- Custom epidemic query box
- Auto-generated executive summary

---

##  Demo

```
Dashboard runs entirely in your browser.
No internet required after initial load.
No database. No backend framework. No build tools.
```

**Live preview:** Open `aeidss_dashboard.html` directly in Chrome/Firefox/Edge.

**With AI features:** Run `python run_aeidss.py` → open `http://localhost:8080`

---

## 🛠️ Tech Stack & Tools

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| HTML5 | — | Structure & semantic markup |
| CSS3 | — | Custom design system, animations, responsive layout |
| JavaScript | ES2020 | All interactivity, chart logic, statistical algorithms |
| Chart.js | 4.4.1 | 15+ chart types (line, bar, bubble, doughnut, radar) |
| Inter | Google Fonts | UI typography |
| JetBrains Mono | Google Fonts | Data/code typography |

### Backend (AI Proxy Server)
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.7+ | Local proxy server |
| `http.server` | stdlib | HTTP server (no frameworks needed) |
| `urllib` | stdlib | API calls to AI providers |
| `json` | stdlib | Request/response handling |
| `socketserver` | stdlib | TCP server with reuse |

### Data
| Source | Format | Size |
|--------|--------|------|
| JHU CSSE COVID-19 Dataset | CSV | ~12MB raw |
| Processed JSON | Embedded in HTML | ~189KB |

### AI Providers Supported
| Provider | Key Format | Free Tier |
|----------|-----------|-----------|
| Groq | `gsk_...` |  Yes |
| Google Gemini | `AIza...` |  Yes |
| OpenRouter | `sk-or-...` |  Yes (free models) |
| OpenAI | `sk-...` | $5 credit |
| Anthropic Claude | `sk-ant-...` | Paid |
| Mistral AI | — | Trial credits |
| Cohere | — | Trial credits |
| Hugging Face | `hf_...` |  Yes |

### Development Tools
- **VS Code** — recommended editor
- **Live Server** (VS Code extension) — optional for hot reload
- **Python 3.7+** — only needed for AI features
- **Git** — version control

---

## Installation & Setup

### Prerequisites
- A modern browser (Chrome, Firefox, Edge, Safari)
- Python 3.7+ (only for AI features)
- Git (to clone the repository)

### Option A — Dashboard Only (No AI, No Setup)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/aeidss.git
cd aeidss

# Just open the file — no installation needed!
# Windows
start aeidss_dashboard.html

# Mac
open aeidss_dashboard.html

# Linux
xdg-open aeidss_dashboard.html
```

All 5 tabs work immediately. No server, no Python, no packages.

---

### Option B — With AI Analysis

#### Step 1: Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/aeidss.git
cd aeidss
```

#### Step 2: Get a free API key
Choose any one:

| Provider | URL | Key Format |
|----------|-----|-----------|
| **Groq** (recommended) | https://console.groq.com | `gsk_...` |
| **Gemini** | https://aistudio.google.com/apikey | `AIza...` |
| **OpenRouter** | https://openrouter.ai | `sk-or-...` |

#### Step 3: Add your key to `run_aeidss.py`
```python
# Open run_aeidss.py and find this line:
API_KEY = "YOUR_API_KEY_HERE"

# Replace with your actual key:
API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"   # Groq example
API_KEY = "AIzaxxxxxxxxxxxxxxxxxx"     # Gemini example
API_KEY = "sk-or-xxxxxxxxxxxxxxxxxx"   # OpenRouter example
```

The server **auto-detects the provider** — no other changes needed.

#### Step 4: Start the server
```bash
python run_aeidss.py
```

Expected output:
```
==========================================================
   AEIDSS — Epidemic Intelligence Dashboard
   Universal AI Proxy · Any Provider Supported
==========================================================

  ✓  API key loaded  Groq  gsk_abc123...xxxx
     Model: llama-3.1-8b-instant
  ✓  Dashboard: aeidss_dashboard.html

  URL  →  http://localhost:8080/aeidss_dashboard.html
```

#### Step 5: Open the dashboard
```
http://localhost:8080/aeidss_dashboard.html
```

>  **Do NOT open the HTML file by double-clicking** if you want AI features. The AI proxy only works via `http://localhost:8080`.

---

### Alternative: Environment Variable (no file editing)

```bash
# Windows PowerShell
$env:AI_API_KEY = "your-key-here"
python run_aeidss.py

# Mac / Linux
export AI_API_KEY="your-key-here"
python run_aeidss.py
```

---

##  Repository Structure

```
aeidss/
│
├── aeidss_dashboard.html          # Complete dashboard (self-contained)
├── run_aeidss.py                  # Universal AI proxy server
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
│
├── data/                          # Raw JHU CSSE dataset files
│   ├── time_series_covid19_confirmed_global.csv
│   ├── time_series_covid19_deaths_global.csv
│   ├── time_series_covid19_recovered_global.csv
│   ├── time_series_covid19_confirmed_US.csv
│   └── time_series_covid19_deaths_US.csv
│
└── scripts/                       # Data processing scripts
    └── process_data.py            # Converts CSV → embedded JSON
```

---

##  Technical Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA PIPELINE                            │
│                                                                 │
│  JHU CSSE CSVs  →  process_data.py  →  JSON (189KB)           │
│  (12MB raw)        (Python script)     (embedded in HTML)       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND ARCHITECTURE                         │
│                                                                 │
│  aeidss_dashboard.html                                          │
│  ├── CSS Design System (custom properties, animations)          │
│  ├── Tab Navigation (lazy initialization)                       │
│  │   ├── Tab 1: Overview                                        │
│  │   │   ├── Chart.js: line (dual-axis)                        │
│  │   │   ├── Chart.js: doughnut (regional)                     │
│  │   │   ├── Chart.js: bar horizontal (log scale)              │
│  │   │   └── Chart.js: bubble (3D viz)                         │
│  │   │                                                          │
│  │   ├── Tab 2: Forecasting                                     │
│  │   │   ├── Holt DES Algorithm (JS)                           │
│  │   │   ├── EMA Forecast Algorithm (JS)                        │
│  │   │   ├── Linear OLS Algorithm (JS)                          │
│  │   │   ├── 95% Confidence Interval (JS)                       │
│  │   │   ├── RMSE / R² Metrics (JS)                            │
│  │   │   └── Chart.js: line + bar + diverging bar              │
│  │   │                                                          │
│  │   ├── Tab 3: Risk Assessment                                 │
│  │   │   ├── Composite Risk Scoring (JS)                        │
│  │   │   ├── SHAP Feature Importance (static weights)           │
│  │   │   ├── Dynamic Search/Filter Table (JS)                   │
│  │   │   └── Chart.js: radar + bar                             │
│  │   │                                                          │
│  │   ├── Tab 4: Early Warning                                   │
│  │   │   ├── Rolling Z-Score Detection (JS)                     │
│  │   │   ├── Scans all 201 countries (JS)                       │
│  │   │   ├── EMA Smoothing (JS)                                 │
│  │   │   └── Chart.js: segmented line + bar + horizontal bar   │
│  │   │                                                          │
│  │   └── Tab 5: Simulation                                      │
│  │       ├── Modified SEIR Model (JS)                           │
│  │       ├── R-Effective Calculator (JS)                        │
│  │       └── Chart.js: dual filled-area                        │
│  │                                                              │
│  └── Explain Panel (pre-written chart explanations)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (optional)
┌─────────────────────────────────────────────────────────────────┐
│                     AI PROXY (run_aeidss.py)                    │
│                                                                 │
│  Browser  →  POST /api/claude                                   │
│           →  Provider Auto-Detection (key prefix matching)      │
│           →  API Call (urllib, no packages)                     │
│           →  Groq / Gemini / OpenAI / OpenRouter / Anthropic   │
│              Mistral / Cohere / Hugging Face                    │
│           ←  JSON Response                                       │
│           ←  Browser renders AI text                            │
└─────────────────────────────────────────────────────────────────┘
```

### Key Algorithms

#### Holt Double Exponential Smoothing
```
Level:    L_t = α·y_t + (1-α)·(L_{t-1} + T_{t-1})
Trend:    T_t = β·(L_t - L_{t-1}) + (1-β)·T_{t-1}
Forecast: F_{t+h} = L_t + h·T_t
CI:       F ± 1.96·σ_residual·√h
```

#### Rolling Z-Score Anomaly Detection
```
Δ_t    = cases_t - cases_{t-1}           (new cases)
μ_t    = mean(Δ[t-w : t])               (rolling mean)
σ_t    = std(Δ[t-w : t])                (rolling std dev)
Z_t    = (Δ_t - μ_t) / σ_t             (z-score)
Alert  = Z_t ≥ threshold                (2.0 / 2.5 / 3.0 / 4.0)
```

#### Modified SEIR Simulation
```
R_eff = R₀ × (1 - mobility×0.5) × (1 - vaccination×0.8) × (1 - masks×0.3)
Growth per week = base_growth × (R_eff / R₀) - testing_effect
```

#### Composite Risk Score
```
Risk = (growth_rate × 0.5) + (CFR × 5) + weekly_cases_factor
Level: High > 20 | Medium > 10 | Low ≤ 10
```

---

##  AI Analysis Setup

The AI analysis tab supports **8 providers** with auto-detection:

```python
# In run_aeidss.py — paste ANY of these:

API_KEY = "gsk_..."        # → Groq      (llama-3.1-8b-instant)
API_KEY = "AIza..."        # → Gemini    (gemini-1.5-flash)
API_KEY = "sk-or-..."      # → OpenRouter (llama free model)
API_KEY = "sk-..."         # → OpenAI    (gpt-4o-mini)
API_KEY = "sk-ant-..."     # → Anthropic  (claude-haiku)
API_KEY = "hf_..."         # → HuggingFace (Mistral-7B)
```

### Free API Keys
| Provider | Get Key | Free Limit |
|----------|---------|-----------|
| **Groq** | https://console.groq.com | Generous free tier |
| **Gemini** | https://aistudio.google.com/apikey | 15 req/min free |
| **OpenRouter** | https://openrouter.ai | Free models available |
| **Hugging Face** | https://huggingface.co/settings/tokens | Free inference API |

---

##  Dataset Citation

```
Dong E, Du H, Gardner L. An interactive web-based dashboard to track
COVID-19 in real time. Lancet Inf Dis. 20(5):533-534. doi:
10.1016/S1473-3099(20)30120-1
```

Data source: https://github.com/CSSEGISandData/COVID-19

---

##  Hackathon Context

This project was developed for a hackathon with the theme:
> *"AI-Powered System for Epidemic Spread Prediction, Risk Assessment, and Intervention Planning"*

**Problem solved:** Epidemiological data is fragmented and existing models focus only on case counts — failing to provide early warnings, causal explanations, or decision support for interventions.

**Solution:** An integrated system combining forecasting, anomaly detection, risk classification, simulation, and AI analysis in a single self-contained HTML file.

---

##  Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Team

Built for the **AI-Powered Epidemic Intelligence Hackathon**

---

<div align="center">

** Star this repo if you found it useful!**

Made with using Chart.js, Python, and real COVID-19 data

</div>
#   A I - P o w e r e d - E p i d e m i c - I n t e l l i g e n c e - D e c i s i o n - S u p p o r t 
 
 
