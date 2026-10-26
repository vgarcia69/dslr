import numpy as np
import sys
import data_utils as du
import describe as d
import math 
import json

training_courses = [
	# "Arithmancy",
	"Astronomy",
	"Herbology",
	# "Defense Against the Dark Arts",
	"Divination",
	"Muggle Studies",
	"Ancient Runes",
	"History of Magic",
	"Transfiguration",
	"Potions",
	# "Care of Magical Creatures",
	"Charms",
	"Flying"
]

def build_Y(ds):
	houses = np.array(ds.houses, dtype=object)
	return (ds.labels == houses[:, None]).astype(float)


def normalize_X(ds):
	X = du.select_courses(ds, training_courses)

	n_rows, n_cols = X.shape

	means = []
	stds = []

	for j in range(n_cols):
		col = X[:, j]
		values = []
		for v in col:
			if not math.isnan(v):
				values.append(v)
		mean = sum(values) / len(values)
		std = d.standard_deviation(values, mean)
		for i in range(n_rows):
			if math.isnan(col[i]):
				col[i] = mean
			col[i] = (col[i] - mean) / std
		means.append(mean)
		stds.append(std)
	return np.c_[np.ones(n_rows), X], means, stds


def sigmoid(z):
	return 1 / (1 + np.exp(-z))


def logistic_regression(X,Y,thetas, ds):
	grades = X
	m = len(X)
	iterations = 100
	learning_rate = 0.1

	for house_i in range(0, len(ds.houses)):
		for _ in range(0, iterations):
			g = np.zeros(X.shape[1], dtype=float)

			for eleve_i in range(0, m):
				score = grades[eleve_i] @ thetas[house_i]
				
				h = sigmoid(score)

				error = h - Y[house_i][eleve_i]

				for matiere_j in range(0, len(grades[0])):
					g[matiere_j] += error * grades[eleve_i][matiere_j]

			for matiere_j in range(0, len(grades[0])):
				thetas[house_i][matiere_j] -= learning_rate * g[matiere_j] / m

	return thetas

def main(path):
	ds = du.load_dataset(path)
	if ds is None:
		return

	Y = build_Y(ds)
	X, means, stds = normalize_X(ds)

	thetas = []
	for house in ds.houses:
		thetas.append(np.zeros(X.shape[1], dtype=float))

	thetas = logistic_regression(X,Y,thetas, ds)

	data = {
		"houses": ds.houses,
		"courses": training_courses,
		"thetas": [theta.tolist() for theta in thetas],
		"means": means,
		"stds": stds,
	}

	with open("training_datas.json", "w") as f:
		json.dump(data, f, indent=4)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 logreg_train.py <dataset.csv>")
		sys.exit(1)
	np.set_printoptions(threshold=sys.maxsize)
	main(sys.argv[1])
