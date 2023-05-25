venv:
	python3 -m venv env

install:
	pip3 install -r requirements.txt

lint:
	flake8 --exclude=env

unit_test:
	pytest -v

tag:
ifdef v
	bash script/tag.sh $(v)
else
	$(error TAG_VERSION is undefined)
endif