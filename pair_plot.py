import sys
import matplotlib.pyplot as plt
import data_utils as du
import pandas as pd

def draw_histogram(ax, course, df, house_colors, house_col="Hogwarts House"):
	for house, color in house_colors.items():
		scores = []
		for _, row in df.iterrows():
			if row[house_col] == house and not pd.isna(row[course]):
				scores.append(row[course])
		ax.hist(scores, bins=20, alpha=0.5, color=color, label=house)

def pair_plot(data_path):
	df = du.read_file(data_path)
	if df is None:
		print("Read_file failed")
		return

	houses = du.get_houses(df)
	courses = du.get_courses(df)
	if houses is None or courses is None:
		print("Something is wrong with houses or courses")
		return

	house_colors = du.get_house_colors(houses)

	n = len(courses)
	fig, axes = plt.subplots(n, n, figsize=(1.5 * n, 1.25 * n), squeeze=False)

	for i in range(0, n):
		for j in range(0, n):
			ax = axes[i][j]
			ax.set_xticks([])
			ax.set_yticks([])
			if i == n - 1:
				ax.set_xlabel(courses[j], fontsize=6)
			if j == 0:
				ax.set_ylabel(courses[i], fontsize=6)
			if (i == j):
				draw_histogram(ax, courses[i], df, house_colors)
			else:
				points = du.get_points(courses[j], courses[i], df)
				if points is None:
					continue
				du.draw_pairs(ax, points, house_colors, size=12)

	axes[0][0].legend(fontsize=4, markerscale=2)
	fig.tight_layout()
	fig.savefig("pair_plot.png", dpi=150)
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 pair_plot.py <dataset.csv>")
		sys.exit(1)
	pair_plot(sys.argv[1])