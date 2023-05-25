venv:
	python3 -m venv env

install: venv
	pip3 install -r requirements.txt

unit_test:
	pytest -v

tag:
ifdef v
	bash script/tag.sh $(v)
else
	$(error TAG_VERSION is undefined)
endif