import pandas as pd

PALETTE = ["#ae0001", "#2a623d", "#222f5b", "#ecb939",
           "#7b3fa0", "#e07b39", "#3a9ad9", "#888888"]


def get_courses(df):
	courses = []
	for col in df.columns:
		if (pd.api.types.is_any_real_numeric_dtype(df[col])):
			courses.append(col)
	return courses


KNOWN_COLORS = {
	"Gryffindor": "#ae0001",
	"Slytherin": "#2a623d",
	"Ravenclaw": "#222f5b",
	"Hufflepuff": "#ecb939",
}


def get_house_colors(houses):
	colors = {}
	for i, house in enumerate(houses):
		colors[house] = KNOWN_COLORS.get(house, PALETTE[i % len(PALETTE)])
	return colors


def get_houses(df, col_name="Hogwarts House"):
	houses = []
	if col_name not in df.columns:
		return None
	for row in df[col_name]:
		if pd.isna(row):
			continue
		if row not in houses:
			houses.append(row)
	return sorted(houses)


def read_file(data_path):
	try:
		df = pd.read_csv(data_path, index_col="Index")
	except Exception:
		df = None
	return df

def get_points(course_x, course_y, df, house="Hogwarts House"):
	points = []
	if course_x not in df.columns or \
		course_y not in df.columns or \
		house not in df.columns:
		return None

	for index, row in df.iterrows():
		if pd.isna(row[course_x]) or pd.isna(row[course_y]):
			continue
		points.append((row[course_x], row[course_y], row[house]))
	return points

def draw_pairs(ax, points, house_colors, size=24):
	for house, color in house_colors.items():
		xs = [x for x, _, h in points if h == house]
		ys = [y for _, y, h in points if h == house]

		ax.scatter(xs, ys, s=size, alpha=0.5, edgecolors="none", color=color, label=house)
