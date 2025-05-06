import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

st.set_page_config(page_title="Advanced Brain Diet Analysis", layout="wide")

st.title("🧠 Advanced Diet & Brain Health Explorer")
st.write("""
This app not only asks about your diet but also loads a sample dataset to  
show how diet scores correlate with cognitive test results.  
_Data sources: Alzheimer’s Association, CDC, National Institute on Aging._
""")

# — Part 1: Your Personal Diet Quiz —
st.header("1. Your Diet Quiz")
score = 0
healthy, unhealthy = 0, 0

def ask(question, options, mapping):
    global score, healthy, unhealthy
    resp = st.selectbox(question, options, key=question)
    delta = mapping.get(resp, 0)
    score += delta
    if delta > 0: healthy += 1
    elif delta < 0: unhealthy += 1

ask(
    "Leafy greens per week?",
    ["0","1–3","4+"],
    {"1–3":1, "4+":2}
)
ask(
    "Berries per week?",
    ["Rarely","1–2","3+"],
    {"1–2":1, "3+":2}
)
ask(
    "Fast food per week?",
    ["3+","1–2","Rarely"],
    {"1–2":-1, "3+":-2}
)
ask(
    "Fish per week?",
    ["Rarely","1–2","3+"],
    {"1–2":1, "3+":2}
)
ask(
    "Sugary snacks/soda?",
    ["Every day","A few times","Rarely"],
    {"A few times":-1, "Every day":-2}
)

percent = int(healthy/(healthy+unhealthy)*100) if (healthy+unhealthy)>0 else 0
st.metric("🥦 Your Diet Score", f"{score} pts", delta=None)
st.metric("🌟 % Healthy Choices", f"{percent}%")

# Pie chart
labels = ['Healthy','Unhealthy']
counts = [healthy, unhealthy]
fig1, ax1 = plt.subplots()
ax1.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# — Part 2: Research-Backed Correlation Analysis —
st.header("2. Research Sample Correlation")
st.write("Below we load a **sample dataset** of participants with diet scores and their cognitive test scores, then compute the correlation.")

@st.cache_data
def load_data():
    df = pd.read_csv("brain_diet_data.csv")
    # Compute same diet score logic on the dataset:
    df['diet_score'] = (
        df['greens'] + df['berries'] - df['fast_food'] + df['fish'] - df['sweets']
    )
    return df

df = load_data()
st.dataframe(df.head(), use_container_width=True)

# Scatter + trend line
x = df['diet_score']
y = df['cognitive_score']
slope, intercept, r, p, std_err = linregress(x, y)

fig2, ax2 = plt.subplots()
ax2.scatter(x, y, alpha=0.7)
ax2.plot(x, slope*x + intercept, 'r--', label=f"r = {r:.2f}")
ax2.set_xlabel("Diet Score")
ax2.set_ylabel("Cognitive Test Score")
ax2.legend()
st.pyplot(fig2)

st.markdown(f"**Pearson correlation:** _r_ = {r:.2f} (p = {p:.3f})")

# — Part 3: References —
st.header("📚 References")
st.markdown("""
1. Alzheimer’s Association. *What Is Alzheimer’s?* https://www.alz.org  
2. CDC. *Diet and Alzheimer’s Disease.* https://www.cdc.gov/alzheimers/diet  
3. National Institute on Aging. *MIND Diet.* https://www.nia.nih.gov/health/mind-diet
""")
