import pandas as pd
import json


# For outputting dataframe, useful for testing
def print_full(x):
    pd.set_option("display.max_rows", len(x))
    print(x)
    pd.reset_option("display.max_rows")


timetable = pd.ExcelFile("./timetable.xlsx")
final_dict = []

for k in range(1, 6):
    df = timetable.parse(f"S{k}")

    # Drop redundant row, clean data
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0)).reset_index(drop=True)
    df.columns.name = None
    df = df.iloc[1:]

    # Define variables for final dictionary
    code = df.iloc[0, 1]
    title = df.iloc[0, 2]
    credits = [df.iloc[0, 3], df.iloc[0, 4], df.iloc[0, 5]]

    sections = []
    section_type = ""
    rooms = []
    instructors = []
    timings = []
    timings_compiled = []

    # Extract data from source Excel
    for i in range(len(df.index)):
        sections.append(df.iloc[i, 6])
        instructors.append(df.iloc[i, 7]) # wrong, fixit

        sections = [item for item in sections if not isinstance(item, float)]
        rooms.append(df.iloc[i, 8])
        rooms = [item for item in rooms if not isinstance(item, float)]

        timings.append(df.iloc[i, 9])
        timings = [item for item in timings if not isinstance(item, float)]

    # Parse timings into list of dictionaries
    for timing in timings:
        dict_timings = None
        timing_list = timing.split()
        dict_timings = {
            "day": [item for item in timing_list if not item.isdigit()],
            "slot": [item for item in timing_list if item.isdigit()],
        }
        timings_compiled.append(dict_timings)

    for section in sections:
        if "P" in section:
            section_type = "practical"
        elif "L" in section:
            section_type = "lecture"
        elif "T" in section:
            section_type = "tutorial"

    sections_compiled = []

    # Figuring out instructors
    

    # Parse sections
    for i in range(len(sections)):
        dict = {
            "section_type": section_type,
            "section_number": sections[i],
            "instructors": [],
            "rooms": rooms[i],
            "timing": timings_compiled[i],
        }

        sections_compiled.append(dict)

    # Final dict
    dict = {
        "course_code": code,
        "course_title": title,
        "credits": {
            "lecture": credits[0],
            "practical": credits[1],
            "units": credits[2],
        },
        "sections": sections_compiled,
    }

    final_dict.append(dict)


# Dump dict into json
with open("data.json", "w") as out_file:
    json.dump(final_dict, out_file, sort_keys=True, ensure_ascii=False, indent=2)
