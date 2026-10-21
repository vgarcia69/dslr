import sys
import math
import pandas as pd
import data_utils as du


STAT_NAMES = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
NAN = float("nan")


def percentile(values, p):
	pos = p * (len(values) - 1)
	bas = int(pos)
	frac = pos - bas
	if bas + 1 < len(values):
		return values[bas] + frac * (values[bas + 1] - values[bas])
	return values[bas]

def standard_deviation(values, mean):
	var = 0
	v_size = len(values)
	if (v_size <= 1):
		return var 
	for v in values:
		ecart = v - mean
		var = var + ecart * ecart
	var = var / (v_size - 1)
	return math.sqrt(var)

def compute_stats(column):
	values = []
	count = 0
	total = 0
	for v in column:
		if not math.isnan(v):
			values.append(v)
			count += 1
			total += v

	if count == 0:
		stats = {name: NAN for name in STAT_NAMES}
		stats["Count"] = 0
		return stats

	sorted_values = sorted(values)
	mean = total / count

	return {
		"Count": count,
		"Mean": mean,
		"Std": standard_deviation(values, mean),
		"Min": sorted_values[0],
		"25%": percentile(sorted_values, 0.25),
		"50%": percentile(sorted_values, 0.50),
		"75%": percentile(sorted_values, 0.75),
		"Max": sorted_values[-1],
	}


def print_stats(stats, cols_per_block=5, width=15):
	names = list(stats.keys())
	for start in range(0, len(names), cols_per_block):
		block = names[start:start + cols_per_block]

		header = f"{'':<8}"
		for name in block:
			header += f"{name[:width - 1]:>{width}}"
		print(header)

		for stat in STAT_NAMES:
			line = f"{stat:<8}"
			for name in block:
				line += f"{stats[name][stat]:>{width}.6f}"
			print(line)
		print()


def describe(path):
	df = du.read_file(path)
	if df is None:
		print("An error occured with the data_file")
		return

	stats = {}
	for col in df.columns:
		if not pd.api.types.is_numeric_dtype(df[col]):
			continue
		stats[col] = compute_stats(df[col])

	if not stats:
		print("No numerical feature found.")
		return

	print_stats(stats)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python describe.py <dataset.csv>")
		sys.exit(1)
	describe(sys.argv[1])
