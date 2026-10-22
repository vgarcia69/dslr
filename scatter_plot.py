import sys
import math
import matplotlib.pyplot as plt
import data_utils as du
import pandas as pd


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
			points = du.get_points(courses[i], courses[j], df)
			r = compute_pearson_coef(points)
			pairs.append((r, points, courses[i], courses[j]))
	pairs.sort(key=lambda pair: abs(pair[0]), reverse=True)
	return pairs


def scatter_plot(data_path):
	df = du.read_file(data_path)
	if df is None:
		return

	courses = du.get_courses(df)
	if len(courses) <= 1:
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

	for p, (_, points, _, _) in enumerate(top):
		ax = axes[p // cols][p % cols]
		du.draw_pairs(ax, points, house_colors, 30)

	axes[0][0].legend(fontsize=7, markerscale=2)
	fig.suptitle(f"Most similar features: {pairs[0][2]} vs {pairs[0][3]}", fontsize=14)
	fig.tight_layout()
	fig.savefig(du.plot_path("scatter_plot.png"), dpi=150)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 scatter_plot.py <dataset.csv>")
		sys.exit(1)
	scatter_plot(sys.argv[1])
