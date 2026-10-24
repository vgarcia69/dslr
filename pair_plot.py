import sys
import matplotlib.pyplot as plt
import data_utils as du


def draw_histogram(ax, course, ds, house_colors):
	for house, color in house_colors.items():
		ax.hist(ds.scores(course, house), bins=20, alpha=0.5, color=color, label=house)


def pair_plot(data_path):
	ds = du.load_dataset(data_path)
	if ds is None:
		print("Read_file failed")
		return

	if not ds.houses or not ds.courses:
		print("Something is wrong with houses or courses")
		return

	house_colors = du.get_house_colors(ds.houses)
	courses = ds.courses

	n = len(courses)
	fig, axes = plt.subplots(n, n, figsize=(1.5 * n, 1.25 * n), squeeze=False)

	for i in range(n):
		for j in range(n):
			ax = axes[i][j]
			ax.set_xticks([])
			ax.set_yticks([])
			if i == n - 1:
				ax.set_xlabel(courses[j], fontsize=6)
			if j == 0:
				ax.set_ylabel(courses[i], fontsize=6)
			if i == j:
				draw_histogram(ax, courses[i], ds, house_colors)
			else:
				xs, ys, labels = ds.points(courses[j], courses[i])
				du.draw_pairs(ax, xs, ys, labels, house_colors, size=12)

	axes[0][0].legend(fontsize=4, markerscale=2)
	fig.tight_layout()
	fig.savefig(du.plot_path("pair_plot.png"), dpi=150)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 pair_plot.py <dataset.csv>")
		sys.exit(1)
	pair_plot(sys.argv[1])
