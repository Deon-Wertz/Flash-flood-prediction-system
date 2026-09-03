import pandas as pd

# ==============================
# LOAD RAINFALL DATA
# ==============================

df = pd.read_csv("../Data/flood_training_data.csv")

df["time"] = pd.to_datetime(df["time"])


# ==============================
# LOAD FLOOD EVENTS
# ==============================

events = pd.read_csv("../Data/flood_events.csv")


# ==============================
# CLEAN EVENT DATES
# ==============================

def clean_event_date(date_value):

    date_value = str(date_value).strip()

    # Handle date ranges like 11-12.07.2021
    if "-" in date_value and "." in date_value:

        parts = date_value.split("-")

        if len(parts) == 2:
            first_day = parts[0]
            rest = parts[1]

            date_value = first_day + "." + rest.split(".", 1)[1]

    return pd.to_datetime(
        date_value,
        dayfirst=True,
        errors="coerce"
    )


events["Date"] = events["Date"].apply(clean_event_date)

# Remove invalid dates
events = events.dropna(subset=["Date"])


# ==============================
# ONLY LOOK AT 2025 EVENTS
# ==============================

events_2025 = events[
    events["Date"].dt.year == 2025
]

print("\n🔥 2025 FLOOD EVENT ANALYSIS\n")

for _, event in events_2025.iterrows():

    event_time = event["Date"]

    print("=" * 70)
    print("EVENT:", event["Event Type"])
    print("Location:", event["Location"])
    print("Reported date:", event_time)

    # Look 12 hours before and after event
    start_time = event_time - pd.Timedelta(hours=12)
    end_time = event_time + pd.Timedelta(hours=12)

    nearby = df[
        (df["time"] >= start_time) &
        (df["time"] <= end_time)
    ]

    if len(nearby) > 0:

        print("\nMaximum rainfall values near event:")

        print(
            nearby[
                [
                    "rainfall_mm_hr",
                    "rainfall_1hr",
                    "rainfall_3hr",
                    "rainfall_6hr",
                    "rainfall_24hr"
                ]
            ].max()
        )

        print("\nRows found:", len(nearby))

    else:
        print("\n⚠️ No rainfall data found near this event.")

print("\n🔥 ANALYSIS COMPLETE!")