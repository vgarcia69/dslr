import sys
import math
import matplotlib.pyplot as plt
import data_utils as du
import pandas as pd


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

def compute_pearson_coef(points):
	if points is None or len(points) == 0:
		return None
	n = len(points)

	x_bar = 0
	y_bar = 0
	for x, y, _ in points:
		x_bar += x
		y_bar += y
	x_bar = x_bar / n
	y_bar = y_bar / n

	num = 0
	sx = 0
	sy = 0
	for x, y, _ in points:
		dx = x - x_bar
		dy = y - y_bar
		num += dx * dy
		sx += dx * dx
		sy += dy * dy

	if sx == 0 or sy == 0:
		return 0
	return num / math.sqrt(sx * sy)

def get_pairs(courses, df):
	pairs = []
	for i in range (0, len(courses)):
		for j in range (i + 1, len(courses)):
			points = get_points(courses[i], courses[j], df)
			r = compute_pearson_coef(points)
			pairs.append((r, points, courses[i], courses[j]))
	pairs.sort(key=lambda pair: abs(pair[0]), reverse=True)
	return pairs

def draw_pairs(ax, r, col_x, col_y, points, house_colors):
	for house, color in house_colors.items():
		xs = [x for x, _, h in points if h == house ]
		ys = [y for _, y, h in points if h == house ]

		ax.scatter(xs, ys, s=6, alpha=0.5, edgecolors="none", color=color, label=house)

def scatter_plot(data_path):
	df = du.read_file(data_path)
	if df is None:
		return

	courses = du.get_courses(df)
	if courses.count <= 1:
		print("There is an issue with courses in data file")
		return

	houses = du.get_houses(df)
	if houses is None:
		print("There is an issue with houses indata file")
		return

	house_colors = du.get_house_colors(houses)

	pairs = get_pairs(courses, df)

	top = pairs[:9]
	n = len(top)
	cols = math.ceil(math.sqrt(n))
	rows = math.ceil(n / cols)

	fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 2.5 * rows), squeeze=False)

	for p, (r, points, col_x, col_y) in enumerate(top):
		ax = axes[p // cols][p % cols]
		draw_pairs(ax, r, col_x, col_y, points, house_colors)

	axes[0][0].legend(fontsize=7, markerscale=2)
	fig.suptitle(f"Most similar features: {pairs[0][2]} vs {pairs[0][3]}", fontsize=14)
	fig.tight_layout()
	plt.show()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 scatter_plot.py <dataset.csv>")
		sys.exit(1)
	scatter_plot(sys.argv[1])
