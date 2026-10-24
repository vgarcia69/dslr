import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import data_utils as du


def compute_pearson_coef(xs, ys):
	n = len(xs)
	if n == 0:
		return 0
	dx = xs - xs.sum() / n
	dy = ys - ys.sum() / n
	sx = (dx * dx).sum()
	sy = (dy * dy).sum()
	if sx == 0 or sy == 0:
		return 0
	return (dx * dy).sum() / math.sqrt(sx * sy)


def get_pairs(ds):
	pairs = []
	courses = ds.courses
	for i in range(len(courses)):
		for j in range(i + 1, len(courses)):
			xs, ys, labels = ds.points(courses[i], courses[j])
			r = compute_pearson_coef(xs, ys)
			pairs.append((r, (xs, ys, labels), courses[i], courses[j]))
	pairs.sort(key=lambda pair: abs(pair[0]), reverse=True)
	return pairs


def scatter_plot(data_path):
	ds = du.load_dataset(data_path)
	if ds is None:
		return

	if len(ds.courses) <= 1:
		print("There is an issue with courses in data file")
		return

	if not ds.houses:
		print("There is an issue with houses in data file")
		return

	house_colors = du.get_house_colors(ds.houses)
	pairs = get_pairs(ds)

	top = pairs[:9]
	n = len(top)
	cols = math.ceil(math.sqrt(n))
	rows = math.ceil(n / cols)

	fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 2.5 * rows), squeeze=False)

	for p, (r, (xs, ys, labels), cx, cy) in enumerate(top):
		ax = axes[p // cols][p % cols]
		du.draw_pairs(ax, xs, ys, labels, house_colors, 30)
		ax.set_xlabel(cx, fontsize=7)
		ax.set_ylabel(cy, fontsize=7)
		ax.set_title(f"r = {r:.3f}", fontsize=8)

	axes[0][0].legend(fontsize=7, markerscale=2)
	fig.suptitle(f"Most similar features: {pairs[0][2]} vs {pairs[0][3]}", fontsize=14)
	fig.tight_layout()
	fig.savefig(du.plot_path("scatter_plot.png"), dpi=150)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 scatter_plot.py <dataset.csv>")
		sys.exit(1)
	scatter_plot(sys.argv[1])
