clean-pyc:
	find . -name "*.pyc" -exec rm -f {} \;
lint:
	flake8 --ignore=E221 . *.py
run:
	python3 bambad.py mac
