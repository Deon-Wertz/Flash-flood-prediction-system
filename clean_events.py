import pandas as pd
import re

# Load flood events
events = pd.read_csv("Data/flood_events.csv")

def parse_event_date(date_string):

    date_string = str(date_string).strip()

    # Handle date range like 11-12.07.2021
    if "-" in date_string and "." in date_string:

        # Extract the final date
        match = re.search(r"(\d{1,2})-(\d{1,2})\.(\d{1,2})\.(\d{4})", date_string)

        if match:
            start_day = match.group(1)
            month = match.group(3)
            year = match.group(4)

            return pd.to_datetime(
                f"{start_day}.{month}.{year}",
                format="%d.%m.%Y"
            )

    # Handle dates with time like:
    # 01.08.2024 0138 hrs

    match = re.search(
        r"(\d{1,2}\.\d{1,2}\.\d{4})\s+(\d{2})(\d{2})\s*hrs",
        date_string
    )

    if match:

        date_part = match.group(1)
        hour = match.group(2)
        minute = match.group(3)

        return pd.to_datetime(
            f"{date_part} {hour}:{minute}",
            format="%d.%m.%Y %H:%M"
        )

    # Handle normal dates
    return pd.to_datetime(
        date_string,
        format="%d.%m.%Y",
        errors="coerce"
    )


# Apply parser
events["Date"] = events["Date"].apply(parse_event_date)

# Show results
print("\nCLEANED EVENTS:\n")
print(events)

# Check failed dates
failed = events[events["Date"].isna()]

print("\nFAILED DATE PARSES:")

if len(failed) == 0:
    print("🔥 ALL DATES PARSED SUCCESSFULLY!")
else:
    print(failed)

# Save cleaned data
events.to_csv(
    "Data/flood_events_cleaned.csv",
    index=False
)

print("\n🔥 CLEANED FILE SAVED!")
print("Data/flood_events_cleaned.csv")