setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "\nTo activate the virtual environment, run 'source venv/bin/activate'\n"

dependency:
	@read -p "Enter the package name to install via pip: " package; \
	pip install $$package && \
	pip freeze | grep $$package >> requirements.txt

prune:
	bash ../script/prune.sh

lint:
	flake8

unit_test:
	pytest -v

func_check:
	python3 ../script/func_check.py

tag:
ifdef v
	bash ../script/tag.sh $(v)
else
	$(error TAG_VERSION is undefined)
endif

func:
	@read -p "Enter the directory name for your function: " dir; \
	func new --name $$dir && bash ../script/funcs.sh $$dir \