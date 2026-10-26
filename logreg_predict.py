import sys
import json
import math
import numpy as np
import data_utils as du


def normalize_X(X, means, stds):
	grades_normalized = []

	for x in X:
		grades = [1.0]
		for i in range(0, len(means)):
			note = x[i]
			if math.isnan(note):
				note = means[i]
			grades.append((note - means[i]) / stds[i])
		grades_normalized.append(grades)

	return np.array(grades_normalized)


def predict_houses(ds, data):
	X = du.select_courses(ds, data["courses"])
	grades_normalized = normalize_X(X, data["means"], data["stds"])
	thetas = np.array(data["thetas"])
	predictions = []

	for student_grades in grades_normalized:
		best_score = float("-inf")
		best_house = ""

		for house_i, house in enumerate(data["houses"]):
			score = student_grades @ thetas[house_i]

			if score > best_score:
				best_score = score
				best_house = house

		predictions.append(best_house)

	return predictions


def write_houses(index, predictions, path="houses.csv"):
	with open(path, "w") as f:
		f.write("Index,Hogwarts House\n")
		for i, house in zip(index, predictions):
			f.write(f"{i},{house}\n")


def main(path, training_data_file):
	try:
		with open(training_data_file, "r") as f:
			data = json.load(f)
	except (OSError, json.JSONDecodeError):
		print(f"Error: cannot read {training_data_file}")
		return

	ds = du.load_dataset(path)
	if ds is None:
		print(f"Error: cannot read {path}")
		return

	for course in data["courses"]:
		if course not in ds.col_index:
			print(f"Error: course '{course}' is missing from {path}")
			return

	predictions = predict_houses(ds, data)
	write_houses(ds.index, predictions)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 logreg_predict.py <dataset_test.csv> <training_datas.json>")
		sys.exit(1)
	main(sys.argv[1], sys.argv[2])
