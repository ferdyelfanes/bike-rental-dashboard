import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")
sns.set(style="darkgrid")

# Memuat data


@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/all_data.csv", parse_dates=["dteday"])
    df["hour"] = df["hr"]
    return df


df = load_data()

# Membuat tab navigasi
st.title("🚴🏻 Bike Rental Analysis Dashboard")
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Casual vs Registered",
    "🌦️ Weather Impact",
    "🗓️ Season & Weather Trends",
    "🏙️ Weekday vs Weekend"
])

# TAB 1: Pola Peminjaman Casual vs Registered
with tab1:
    st.header("📊 Rental Behavior: Registered vs Casual Users")
    col1, col2 = st.columns(2)
    with col1:
        start_date1 = st.date_input(
            "📆 Start Date", df["dteday"].min(), key="date1")
    with col2:
        end_date1 = st.date_input(
            "📆 End Date", df["dteday"].max(), key="date2")

    filtered_df1 = df[
        (df["dteday"] >= pd.to_datetime(start_date1)) &
        (df["dteday"] <= pd.to_datetime(end_date1))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df1, x="hour", y="casual_hour",
                 label="Casual Users", marker="o", ax=ax)
    sns.lineplot(data=filtered_df1, x="hour", y="registered_hour",
                 label="Registered Users", marker="o", ax=ax)
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Rentals")
    ax.set_title("Hourly Rental Trends: Registered vs Casual Users")
    ax.legend()
    st.pyplot(fig)

    #  Summary & Caption
    st.caption(
        "🔍 This visualization highlight the distinct rental patterns of registered and casual users throughout the day.")
    st.markdown("### 📌 Summary")
    st.write(
        "- 🏢 **Registered Users:** Rental surge during commuting hours (morning and evening rush).")
    st.write("- 🚴 **Casual Users:** Peak activity occurs during midday, likely due to leisured-based usage.")

# TAB 2: Pengaruh Kondisi Cuaca
with tab2:
    st.header("🌦️ How Weather Affects Bike Rentals")
    col1, col2 = st.columns(2)
    with col1:
        start_date2 = st.date_input(
            "📆 Start Date", df["dteday"].min(), key="date3")
    with col2:
        end_date2 = st.date_input(
            "📆 End Date", df["dteday"].max(), key="date4")

    filtered_df2 = df[
        (df["dteday"] >= pd.to_datetime(start_date2)) &
        (df["dteday"] <= pd.to_datetime(end_date2))
    ]

    pivot_weather = filtered_df2.groupby(["hour", "weathersit_day"])[
        "cnt_hour"].mean().unstack()

    fig, ax = plt.subplots(figsize=(11, 6))
    pivot_weather.plot(ax=ax, linewidth=2.5)

    label_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain"}
    handles, labels = ax.get_legend_handles_labels()
    new_labels = [label_mapping.get(int(label), label) for label in labels]
    ax.legend(handles, new_labels, title="Weather Condition")

    ax.set_title(
        "Effect of Weather on Bike Rentals Throughout the Day")
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Average Number of Rentals")
    ax.set_xticks(range(0, 24, 5))

    st.pyplot(fig)

    # 📌 Summary & Caption
    st.caption(
        "🌦️ Inclement weather significantly reduces bike rental activity, impacting both registered and casual users.")
    st.markdown("### 📌 Summary")
    st.write("- ☀️ **Clear Weather:** Rental volume remain high throughout the day.")
    st.write(
        "- 🌧 **Light Rain:** Noticable decline in rentals, particularly during peak hours.")

# # TAB 3: Seasonal and Weather-Based Rental Trends
with tab3:
    st.header("🗓️ Seasonal & Weather-Dependent Rental Variations")
    col1, col2 = st.columns(2)
    with col1:
        start_date3 = st.date_input(
            "📆 Start Date", df["dteday"].min(), key="date5")
    with col2:
        end_date3 = st.date_input(
            "📆 End Date", df["dteday"].max(), key="date6")

    filtered_df3 = df[
        (df["dteday"] >= pd.to_datetime(start_date3)) &
        (df["dteday"] <= pd.to_datetime(end_date3))
    ]

    # Layout: Two Visualizations Side by Side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Rental Trends by Season")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="season_day", y="cnt_day", data=filtered_df3, hue="season_day",
                    palette="tab10", legend=False, ax=ax)
        ax.set_xlabel("Season")
        ax.set_ylabel("Average Number of Rentals")
        ax.set_title("Bike Rental Patterns Across Seasons")
        ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
        st.pyplot(fig)

    with col2:
        st.subheader("☁️ Impact of Weather Conditions")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="weathersit_day", y="cnt_day", data=filtered_df3, hue="weathersit_day",
                    palette="tab10", legend=False, ax=ax)
        ax.set_xlabel("Weather Condition")
        ax.set_ylabel("Average Number of Rentals")
        ax.set_title("Effect of Weather on Bike Rentals")
        ax.set_xticklabels(["Clear", "Cloudy", "Light Rain"])
        st.pyplot(fig)

    # 📌 Summary & Caption
    st.caption("🌍 Seasonal and weather conditions significantly influence bike rental volumes, with fall being the most active period.")
    st.markdown("### 📌 Summary")
    st.write(
        "- 🍂 **Fall:** Peak rental volumes due to favorable weather conditions.")
    st.write(
        "- 🌱 **Spring:** Marked decrease in activity among the seasons.")
    st.write("- 🌦 **Weather Conditions:** Clear days encourage more rentals, whereas rainy conditions lead to a sharp decline.")

# TAB 4: Perbandingan Weekdays vs Weekends
with tab4:
    st.header("🏙️ Comparing Weekday and Weekend Rental Trends")
    col1, col2 = st.columns(2)
    with col1:
        start_date4 = st.date_input(
            "📆 Start Date", df["dteday"].min(), key="date7")
    with col2:
        end_date4 = st.date_input(
            "📆 End Date", df["dteday"].max(), key="date8")

    filtered_df4 = df[
        (df["dteday"] >= pd.to_datetime(start_date4)) &
        (df["dteday"] <= pd.to_datetime(end_date4))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df4[filtered_df4["workingday_hour"] == 1],
                 x="hour", y="cnt_hour", label="Weekdays", marker="o", ax=ax)
    sns.lineplot(data=filtered_df4[filtered_df4["workingday_hour"] == 0],
                 x="hour", y="cnt_hour", label="Weekends", marker="o", ax=ax)
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Rentals")
    ax.set_title("Rental Patterns: Weekdays vs Weekends")
    ax.legend()
    st.pyplot(fig)

    # 📌 Summary & Caption
    st.caption(
        "📅 Rental patterns shift based on the day of the week, with weekends exhibiting a more evenly distributed usage pattern.")
    st.markdown("### 📌 Summary")
    st.write("- 🏢 **Weekdays:** Rentals peak during commuting hours")
    st.write(
        "- 🚴‍♂️ **Weekends:** More consistent usage throughout the day")

st.caption("© 2025 Data Moves, Just Like Bikes | Elfanes 🚀")
