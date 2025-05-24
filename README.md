# 🌤️ Knowledge-Based Weather Prediction System

This is a rule-based expert system that predicts weather conditions based on user inputs such as temperature, rain expectation, storm chances, and cloud levels. The system is implemented using Python and integrates Prolog logic through the `pyswip` library.

---
## 👥 Team Members

- **Raheel Ahmed**
- **Hasnain Shensha**
- **Hassaan Khalid**
- **Sara Akmal**

of Comsats University Islamabad, Wah Campus. Made as a semester project for subject Artificial Intelligence.

---
## 🧠 How It Works

The system uses a knowledge base of weather rules written in Prolog to analyze environmental inputs and return a prediction along with a reasoning explanation.

### ✅ Inputs Taken:
- 🌡️ Temperature (in Celsius)
- ☔ Is rain expected? (`yes` / `no`)
- 🌩️ Is a storm expected? (`yes` / `no`)
- ☁️ Cloud level (`low`, `medium`, `high`)

### 🔍 Output:
- A **weather prediction** (e.g., `sunny`, `stormy`, `partly_sunny`, etc.)
- A **reasoning chain** (e.g., `"Hot temperature + humid + low clouds"`)

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Prolog** (via [`pyswip`](https://github.com/yuce/pyswip))
- Optional: **Tkinter** (for GUI, if added later)

---

## 📦 Setup Instructions

### 1. Install Requirements
Make sure you have:
- Python 3.x
- SWI-Prolog installed on your system
- Required Python libraries

```bash
pip install pyswip
```

## ▶️ How to Run

Run the weather predictor using this **bash command**:
- `python weather-predictor.py`
