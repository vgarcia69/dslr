import os
import numpy as np
import pandas as pd

PLOTS_DIR = "plots"
HOUSE_COL = "Hogwarts House"

PALETTE = ["#ae0001", "#2a623d", "#222f5b", "#ecb939",
           "#7b3fa0", "#e07b39", "#3a9ad9", "#888888"]

KNOWN_COLORS = {
	"Gryffindor": "#ae0001",
	"Slytherin": "#2a623d",
	"Ravenclaw": "#222f5b",
	"Hufflepuff": "#ecb939",
}


class Dataset:
	"""
	Lit le CSV une seule fois avec pandas, puis range tout dans des tableaux numpy.

	X        : np.ndarray float, shape (n_eleves, n_matieres). NaN = note manquante.
	           ligne i   -> un eleve
	           colonne j -> une matiere (courses[j])
	labels   : np.ndarray, shape (n_eleves,). La maison de chaque eleve (NaN si inconnue).
	courses  : liste des noms de matieres, dans l'ordre des colonnes de X.
	houses   : liste triee des maisons presentes.
	col_index: dict nom_de_matiere -> numero de colonne dans X.
	"""

	def __init__(self, df, house_col=HOUSE_COL):
		self.courses = []
		for col in df.columns:
			if col != house_col and pd.api.types.is_any_real_numeric_dtype(df[col]):
				self.courses.append(col)

		self.col_index = {name: j for j, name in enumerate(self.courses)}
		self.X = df[self.courses].to_numpy(dtype=float)

		if house_col in df.columns:
			self.labels = df[house_col].to_numpy(dtype=object)
			known = self.labels[pd.notna(self.labels)]
			self.houses = sorted(set(known))
		else:
			self.labels = np.full(len(df), np.nan, dtype=object)
			self.houses = []

	def __len__(self):
		return self.X.shape[0]

	def column(self, course):
		"""Toutes les notes d'une matiere (NaN compris)."""
		return self.X[:, self.col_index[course]]

	def scores(self, course, house=None):
		"""Notes d'une matiere sans les NaN, eventuellement filtrees sur une maison."""
		col = self.column(course)
		mask = ~np.isnan(col)
		if house is not None:
			mask &= (self.labels == house)
		return col[mask]

	def points(self, course_x, course_y):
		"""(xs, ys, labels) des eleves qui ont une note dans les DEUX matieres."""
		x = self.column(course_x)
		y = self.column(course_y)
		mask = ~np.isnan(x) & ~np.isnan(y)
		return x[mask], y[mask], self.labels[mask]


def load_dataset(data_path):
	try:
		df = pd.read_csv(data_path, index_col="Index")
	except Exception:
		return None
	return Dataset(df)


def get_house_colors(houses):
	colors = {}
	for i, house in enumerate(houses):
		colors[house] = KNOWN_COLORS.get(house, PALETTE[i % len(PALETTE)])
	return colors


def draw_pairs(ax, xs, ys, labels, house_colors, size=24):
	for house, color in house_colors.items():
		m = (labels == house)
		ax.scatter(xs[m], ys[m], s=size, alpha=0.5, edgecolors="none", color=color, label=house)


def plot_path(filename):
	os.makedirs(PLOTS_DIR, exist_ok=True)
	return os.path.join(PLOTS_DIR, filename)
