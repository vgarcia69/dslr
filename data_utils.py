import pandas as pd

PALETTE = ["#ae0001", "#2a623d", "#222f5b", "#ecb939",
           "#7b3fa0", "#e07b39", "#3a9ad9", "#888888"]


def get_courses(df):
	courses = []
	for col in df.columns:
		if (pd.api.types.is_any_real_numeric_dtype(df[col])):
			courses.append(col)
	return courses


def get_house_colors(houses):
    colors = {}
    for i, house in enumerate(houses):
        colors[house] = PALETTE[i % len(PALETTE)]
    return colors


def get_houses(df, col_name="Hogwarts House"):
	houses = []
	if col_name not in df.columns:
		return None
	for row in df[col_name]:
		if row not in houses:
			houses.append(row)
	return houses


def read_file(data_path):
	try:
		df = pd.read_csv(data_path, index_col="Index")
	except Exception:
		df = None
	return df