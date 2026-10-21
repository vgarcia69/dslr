import sys
import pandas as pd
import matplotlib.pyplot as plt
import data_utils as du

def histogram(path):
	df = du.read_file(path)
	if df is None:
		print("An error occured with the data_file")
		return

	courses = du.get_courses(df)
	houses = du.get_houses(df)

	if houses is None or courses is None:
		print("There is an issue with the data file")
		return

	plt.figure(figsize=(16,12))
	i = 1
	for course in courses:
		plt.subplot(4,4,i)
		for house in houses:
			score = []
			for row_i, row_data in df.iterrows():
				if row_data["Hogwarts House"] == house:
					if not pd.isna(row_data[course]):
						score.append(row_data[course])
			plt.hist(score, bins=20,alpha=0.5, label=house)
		i+=1
		plt.legend(fontsize=6)
		plt.title(course)
	plt.tight_layout()
	plt.show()
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 histogram.py <dataset.csv>")
		sys.exit(1)
	histogram(sys.argv[1])
