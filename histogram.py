import sys
import pandas as pd
import matplotlib.pyplot as plt

def histogram(path):
	try:
		df = pd.read_csv(path, index_col="Index")
	except Exception as e:
		print(f"Error: cannot read '{path}': {e}")
		sys.exit(1)

	courses = []
	houses = []

	for col in df.columns:
		if col == "Hogwarts House":
			for row in df[col]:
				if row not in houses and not pd.isna(row):
					houses.append(row)
		if pd.api.types.is_any_real_numeric_dtype(df[col]):
			courses.append(col)
			
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
