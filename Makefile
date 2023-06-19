setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "\nTo activate the virtual environment, run 'source venv/bin/activate'\n"

dirs = . collectors processors loaders

setup_repo:
	for i in $(dirs); do \
		${MAKE} -C $$i setup; \
	done
	code .vscode/bootcamp_benchmark.code-workspace

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

open_collectors:
	code collectors/.vscode/collectors_bootcamp_benchmark.code-workspace

open_processors:
	code processors/.vscode/processors_bootcamp_benchmark.code-workspace

open_loaders:
	code loaders/.vscode/loaders_bootcamp_benchmark.code-workspace