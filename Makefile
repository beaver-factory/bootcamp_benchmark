setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "\nTo activate the virtual environment, run 'source venv/bin/activate'\n"

dependency:
	@read -p "Enter the package name to install via pip: " package; \
	pip install $$package && \
	pip freeze | grep $$package >> requirements.txt

lint:
	flake8

tag:
ifdef v
	bash script/tag.sh $(v)
else
	$(error TAG_VERSION is undefined)
endif