VENV     = venv
PYTHON   = $(VENV)/bin/python
PIP      = $(VENV)/bin/pip
TRAIN    = datasets/dataset_train.csv
TEST     = datasets/dataset_test.csv
WEIGHTS  = weights.csv
STAMP    = $(VENV)/.installed
PLOTS    = plots
OPEN     = $(shell command -v open 2>/dev/null || command -v xdg-open 2>/dev/null)

.PHONY: help venv install venv-on venv-off describe histogram scatter pair train predict all clean fclean re

help:
	@echo "make venv       -> crée le venv et installe les dépendances"
	@echo "make venv-on    -> ouvre un shell avec le venv activé (exit pour en sortir)"
	@echo "make venv-off   -> rappel pour désactiver le venv"
	@echo "make describe   -> describe.py sur $(TRAIN)"
	@echo "make histogram  -> histogram.py"
	@echo "make scatter    -> scatter_plot.py"
	@echo "make pair       -> pair_plot.py"
	@echo "make train      -> logreg_train.py"
	@echo "make predict    -> logreg_predict.py"
	@echo "make all        -> train puis predict"
	@echo "make clean / fclean / re"

$(PYTHON):
	python3 -m venv $(VENV)

$(STAMP): $(PYTHON)
	$(PIP) install --upgrade pip
	$(PIP) install numpy pandas matplotlib
	touch $(STAMP)

venv: $(STAMP)

install: venv

venv-on: $(STAMP)
	@echo "venv activé — tape 'exit' pour le désactiver"
	@VIRTUAL_ENV=$(CURDIR)/$(VENV) PATH=$(CURDIR)/$(VENV)/bin:$$PATH $$SHELL -i

venv-off:
	@echo "Dans un shell 'make venv-on' : tape 'exit'"
	@echo "Si tu as fait 'source venv/bin/activate' : tape 'deactivate'"

describe: $(STAMP)
	$(PYTHON) describe.py $(TRAIN)

histogram: $(STAMP)
	$(PYTHON) histogram.py $(TRAIN)
	@[ -n "$(OPEN)" ] && $(OPEN) $(PLOTS)/histogram.png || true

scatter: $(STAMP)
	$(PYTHON) scatter_plot.py $(TRAIN)
	@[ -n "$(OPEN)" ] && $(OPEN) $(PLOTS)/scatter_plot.png || true

pair: $(STAMP)
	$(PYTHON) pair_plot.py $(TRAIN)
	@[ -n "$(OPEN)" ] && $(OPEN) $(PLOTS)/pair_plot.png || true

train: $(STAMP)
	$(PYTHON) logreg_train.py $(TRAIN)

predict: $(STAMP)
	$(PYTHON) logreg_predict.py $(TEST) $(WEIGHTS)

all: train predict

clean:
	rm -rf __pycache__

fclean: clean
	rm -f $(WEIGHTS) houses.csv
	rm -rf $(PLOTS)

re: fclean all
