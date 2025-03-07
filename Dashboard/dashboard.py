import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi awal dashboard
st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")
sns.set_theme(style="darkgrid")

# Load dataset


@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv", parse_dates=["dteday"])
    df["hour"] = df["hr"]
    return df


df = load_data()

# Sidebar - Filter Data
st.sidebar.header("🔎 Filter Data")
start_date = st.sidebar.date_input("📅 Start Date", df["dteday"].min())
end_date = st.sidebar.date_input("📅 End Date", df["dteday"].max())

# Mapping musim
season_mapping = {1: "Spring 🌱", 2: "Summer☀️", 3: "Fall 🍂", 4: "Winter ❄️"}
df["season_label"] = df["season_hour"].map(season_mapping)
season_options = df["season_label"].unique().tolist()
selected_season = st.sidebar.multiselect(
    "🌍 Select Season", season_options, default=season_options)

# Mapping cuaca
weather_mapping = {1: "Clear☀️", 2: "Cloudy⛅️",
                   3: "Light Rain🌧️", 4: "Heavy Rain⚡️"}
df["weather_label"] = df["weathersit_hour"].map(weather_mapping)
weather_options = df["weather_label"].unique().tolist()
selected_weather = st.sidebar.multiselect(
    "🌦️ Select Weather", weather_options, default=weather_options)

# Pilihan hari kerja atau akhir pekan
day_type = st.sidebar.radio("📅 Day Type", ["All", "Weekday", "Weekend"])

# Filter data berdasarkan pilihan user
filtered_df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date)) &
    (df["weather_label"].isin(selected_weather)) &
    (df["season_label"].isin(selected_season))
]

if day_type == "Weekday":
    filtered_df = filtered_df[filtered_df["workingday_hour"] == 1]
elif day_type == "Weekend":
    filtered_df = filtered_df[filtered_df["workingday_hour"] == 0]

# Dashboard Title
st.title("🚴 Bike Rental Analysis Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Rental Patterns", "📊 RFM Analysis", "🌍 Weather & Seasons", "📅 Weekday vs Weekend"])

with tab1:
    st.subheader(
        "⏰ Bike Rental Patterns by Hour (Casual vs Registered Users)")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x="hr", y="casual_hour",
                 label="Casual Users", marker="o", ax=ax, color="#1f77b4")
    sns.lineplot(data=df, x="hr", y="registered_hour",
                 label="Registered Users", marker="o", ax=ax, color="#ff7f0e")

    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Rentals")
    ax.set_title("Bike Rental Patterns by Hour")
    ax.legend()

    st.pyplot(fig)

with tab2:
    st.subheader("📊 Customer Behavior Based on RFM Metrics")

    recency_days = (df["dteday"].max() - df["dteday"]).dt.days
    frequency_data = df.groupby("weekday_day")["dteday"].count().reset_index()
    monetary_data = df.groupby("weekday_day")["cnt_day"].sum().reset_index()

    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Average Recency (Days)", round(recency_days.mean(), 1))
    col2.metric("🔁 Average Frequency", round(
        frequency_data["dteday"].mean(), 1))
    col3.metric("💰 Average Rental Count", round(
        monetary_data["cnt_day"].mean(), 1))

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    color = "#1f77b4"

    sns.histplot(recency_days, bins=30, kde=True, color=color, ax=ax[0])
    ax[0].set_title("Distribusi Recency")
    ax[0].set_xlabel("Hari Sejak Peminjaman Terakhir")
    ax[0].set_ylabel("Frekuensi Pelanggan")

    sns.barplot(x="weekday_day", y="dteday",
                data=frequency_data, color=color, ax=ax[1])
    ax[1].set_title("Frekuensi Peminjaman Berdasarkan Hari")
    ax[1].set_xlabel("Hari dalam Seminggu")
    ax[1].set_ylabel("Jumlah Minggu Peminjaman")

    sns.barplot(x="weekday_day", y="cnt_day",
                data=monetary_data, color=color, ax=ax[2])
    ax[2].set_title("Total Peminjaman Berdasarkan Hari")
    ax[2].set_xlabel("Hari dalam Seminggu")
    ax[2].set_ylabel("Total Peminjaman")

    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    st.subheader("🌍 Impact of Weather and Season on Rentals")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x="weather_label", y="cnt_day",
                data=filtered_df, ax=ax, palette=["#1f3c88", "#72a2c0", "#ff7f0e", "#d62728"])
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Number of Rentals")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x="season_label", y="cnt_day",
                data=filtered_df, ax=ax, palette="viridis")
    ax.set_xlabel("Season")
    ax.set_ylabel("Number of Rentals")
    st.pyplot(fig)

with tab4:
    st.subheader("📅 Rental Patterns on Weekdays vs Weekends")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df[df["workingday_hour"] == 1], x="hr",
                 y="cnt_hour", label="Weekday", marker="o", ax=ax, color="#ff7f0e")
    sns.lineplot(data=df[df["workingday_hour"] == 0], x="hr",
                 y="cnt_hour", label="Weekend", marker="o", ax=ax, color="#1f77b4")

    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Rentals")
    ax.set_title("Comparison of Bike Rentals: Weekdays vs Weekends")
    ax.legend()

    st.pyplot(fig)

# Ringkasan Akhir
st.markdown("#### **📌 Summary**")
st.write("""
- **📈 Rental Patterns:** Bike rentals peak during morning and evening rush hours.
- **📊 RFM Analysis:** The average customer exhibits varying rental durations, with certain user segments displaying higher frequency patterns.
- **🌍 Impact of Weather:** Adverse weather conditions significantly reduce the number of rentals.
- **📅 Weekday vs Weekend Trends:** Rentals are higher on weekends, with a more evenly distributed usage pattern throughout the day.
""")

st.caption("© 2025 Data Moves, Just Like Bikes | Elfanes 🚀")
