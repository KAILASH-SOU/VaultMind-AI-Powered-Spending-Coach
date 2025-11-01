# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="💸 VaultMind — AI-Powered Spending Coach", layout="wide")

# -----------------------------------------------------------------------------
# LOAD ENV & CONFIGURE GEMINI
# -----------------------------------------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------------------------------------------------------
# HELPER: LOAD LATEST DATA
# -----------------------------------------------------------------------------
@st.cache_data(ttl=10)
def load_latest():
    import pandas as pd

    try:
        df = pd.read_csv("transactions.csv")
    except FileNotFoundError:
        st.warning("⚠️ No transaction file found — creating a fresh one.")
        df = pd.DataFrame(columns=["Date","Merchant","Category","Amount","Payment_Method","Account_Balance"])
        df.to_csv("transactions.csv", index=False)

    # 🧠 Force convert Date column to datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with invalid dates
    df = df.dropna(subset=["Date"])

    df.sort_values("Date", inplace=True)
    return df


df = load_latest()

# -----------------------------------------------------------------------------
# SIDEBAR: ADD NEW TRANSACTION
# -----------------------------------------------------------------------------
st.sidebar.header("➕ Add a New Transaction")

date = st.sidebar.date_input("Date", datetime.today())
merchant = st.sidebar.text_input("Merchant", "Amazon")
category = st.sidebar.text_input("Category", "Shopping")
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=10.0)
payment = st.sidebar.text_input("Payment Method", "Credit Card")

if st.sidebar.button("Add Transaction"):
    new_row = pd.DataFrame({
        "Date": [pd.to_datetime(date)],
        "Merchant": [merchant],
        "Category": [category],
        "Amount": [amount],
        "Payment_Method": [payment],
        "Account_Balance": [max(0, df["Account_Balance"].mean() - amount if not df.empty else 50000 - amount)]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("transactions.csv", index=False)
    st.sidebar.success("✅ Transaction added successfully!")

# -----------------------------------------------------------------------------
# MAIN DASHBOARD
# -----------------------------------------------------------------------------
st.title("🤖 VaultMind — AI-Powered Spending Coach")

# --- Privacy notice ---
st.info("🔒 **Privacy Notice:** This demo uses synthetic / local data only. No personal or financial data is uploaded or stored externally.")

# -----------------------------------------------------------------------------
# VISUALIZATION SECTION
# -----------------------------------------------------------------------------
st.subheader("📊 Spending Overview")

if df.empty:
    st.warning("No data available yet. Add transactions from the sidebar or start the simulator.")
else:
    col1, col2 = st.columns(2)
    with col1:
        monthly_spend = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
        fig, ax = plt.subplots()
        monthly_spend.plot(kind="bar", ax=ax, color="royalblue")
        ax.set_title("Monthly Spending (₹)")
        st.pyplot(fig)

    with col2:
        cat_spend = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        fig2, ax2 = plt.subplots()
        cat_spend.plot(kind="barh", ax=ax2, color="mediumseagreen")
        ax2.set_title("Spending by Category")
        st.pyplot(fig2)

# -----------------------------------------------------------------------------
# SMART ALERT ENGINE
# -----------------------------------------------------------------------------
st.subheader("⚠️ Smart Alerts")

alerts = []
if not df.empty:
    recent_7 = df[df["Date"] > (datetime.today() - timedelta(days=7))]

    # High weekly spending alert
    if len(recent_7) > 0:
        last_week_spend = recent_7["Amount"].sum()
        avg_week_spend = df.groupby(df["Date"].dt.isocalendar().week)["Amount"].sum().mean()
        if last_week_spend > 1.5 * avg_week_spend:
            alerts.append(f"🚨 You spent ₹{int(last_week_spend)} last week — 50% higher than usual!")

    # Top category alert
    if len(df) > 0:
        top_cat = df.groupby("Category")["Amount"].sum().idxmax()
        if top_cat.lower() in ["shopping", "food", "entertainment"]:
            alerts.append(f"🛒 Your top spending category is **{top_cat}** — consider setting a weekly limit.")

    # Duplicate subscription detection
    dup_subs = df[df["Category"].str.lower().eq("subscriptions")]
    if not dup_subs.empty:
        dup_check = dup_subs.groupby(["Merchant", df["Date"].dt.date])["Amount"].count()
        for (m, d), c in dup_check.items():
            if c > 1:
                alerts.append(f"⚠️ Possible duplicate subscription payment detected for **{m}** on {d}.")

if len(alerts) == 0:
    st.success("✅ No financial anomalies detected — great job staying consistent!")
else:
    for alert in alerts:
        st.warning(alert)

# -----------------------------------------------------------------------------
# AI COACHING SECTION
# -----------------------------------------------------------------------------
st.subheader("💬 AI Personalized Coach")

if st.button("Get Smart Advice 🧠"):
    if df.empty:
        st.error("Please add some transactions first.")
    else:
        total_spend = round(df["Amount"].sum(), 2)
        avg_daily = round(df.groupby("Date")["Amount"].sum().mean(), 2)
        latest_txn = df.sort_values("Date").iloc[-1]

        prompt = f"""
        You are an empathetic AI financial coach.
        The user’s transaction summary:
        - Total Spend: ₹{total_spend}
        - Average Daily Spend: ₹{avg_daily}
        - Last Transaction: ₹{latest_txn['Amount']} at {latest_txn['Merchant']} ({latest_txn['Category']})
        Alerts: {', '.join(alerts) if alerts else 'None'}

        Analyze patterns and give personalized, motivational feedback in <200 words>:
        - 1 tip on spending optimization
        - 1 saving strategy
        - 1 short motivational line
        Tone: friendly, practical, human.
        """

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            st.success("🧭 AI Coach Advice:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini API error: {e}")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("💡 Built by Kailash Sou • Phase 3 — Agentic AI Finance Coach")
