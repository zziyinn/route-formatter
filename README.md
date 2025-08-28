# 🧭 Route Formatter

A simple tool to solve the issue of messy driver ID formats provided by DSP.  
Just paste the original text → the tool automatically parses and reformats it → copy the standardized output directly into your pickup sheet.  

## ✨ Features
- Automatically recognizes multiple title formats: `X route ... date`, `X号线`, `X号`
- Supports two segment formats: `a-b v` and `v(a-b)`
- By default only outputs **Lines 20–31**
- Two sorting modes:
  - **numeric**: fixed order 20 → 31
  - **encounter**: order of appearance in the input text

## 🚀 Online Demo
No installation required. Try it directly here:  
👉 [Route Formatter on Streamlit](https://yourname-route-formatter.streamlit.app)

## 🛠️ Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/yourname/route-formatter.git
   cd route-formatter
