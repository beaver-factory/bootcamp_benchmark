venv:
	python3 -m venv env

install:
	pip3 install -r requirements.txt

lint:
	flake8

unit_test:
	pytest -v

func_check:
	python3 script/func_check.py

tag:
ifdef v
	bash script/tag.sh $(v)
else
	$(error TAG_VERSION is undefined)
endif

func:
ifdef dir
	func new --name $(dir) && bash script/funcs.sh $(dir)
else
	$(error directory is undefined)
endif