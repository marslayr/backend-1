import pandas as pd
import numpy as np
import json


def print_full(x):
    pd.set_option("display.max_rows", len(x))
    print(x)
    pd.reset_option("display.max_rows")


timetable = pd.ExcelFile("./timetable.xlsx")

df1 = timetable.parse("S1")
df1.columns = df1.iloc[0]
df1 = df1.reindex(df1.index.drop(0)).reset_index(drop=True)
df1.columns.name = None

df1 = df1.iloc[1:]

code = df1.iloc[0, 1]
title = df1.iloc[0, 2]
credits = [df1.iloc[0, 3], df1.iloc[0, 4], df1.iloc[0, 5]]

sections = []
section_type = ""
rooms = []
instructors = []
timings = []
timings_compiled = []
breaks = []
k = 0

for i in range(len(df1.index)):


    instructors.append(df1.iloc[i, 7])
    instructors = [item for item in instructors]

    sections.append(df1.iloc[i, 6])
    
    sections = [item for item in sections if not isinstance(item, float)]
    rooms.append(df1.iloc[i, 8])
    rooms = [item for item in rooms if not isinstance(item, float)]


    timings.append(df1.iloc[i, 9])
    timings = [item for item in timings if not isinstance(item, float)]
    

for timing in timings:
    dict_timings = None
    timing_list = timing.split()
    
    dict_timings = {
        "day": timing_list[0],
        "slot": [int(timing_list[1]), int(timing_list[2])]
    }
    timings_compiled.append(dict_timings)
    
print(timings_compiled)
for section in sections:
    if "P" in section:
        section_type = "practical"
    elif "L" in section:
        section_type = "lecture"

sections_compiled = []

    
for i in range(len(sections)):
    dict = {
        "section_type": section_type,
        "section_number": sections[i],
        "instructors": [],
        "rooms": rooms[i],
        "timing": timings_compiled[i],
    }

    sections_compiled.append(dict)

dict = [
    {
        "course_code": code,
        "course_title": title,
        "credits": {
            "lecture": credits[0],
            "practical": credits[1],
            "units": credits[2],
        },
        "sections": sections_compiled,
    }
]

# print(df1.iloc[:, 7])

# print(json.dumps(dict, indent=4))