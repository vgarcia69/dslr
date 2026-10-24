import sys
import matplotlib.pyplot as plt
import data_utils as du


def histogram(path):
	ds = du.load_dataset(path)
	if ds is None:
		print("An error occured with the data_file")
		return

	if not ds.houses or not ds.courses:
		print("There is an issue with the data file")
		return

	house_colors = du.get_house_colors(ds.houses)

	plt.figure(figsize=(16, 12))
	for i, course in enumerate(ds.courses, start=1):
		plt.subplot(4, 4, i)
		for house, color in house_colors.items():
			plt.hist(ds.scores(course, house), bins=20, alpha=0.5, color=color, label=house)
		plt.legend(fontsize=6)
		plt.title(course)
	plt.tight_layout()
	plt.savefig(du.plot_path("histogram.png"), dpi=150)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 histogram.py <dataset.csv>")
		sys.exit(1)
	histogram(sys.argv[1])
