#!/bin/bash

# build new reqs from current project
pipreqs ./ --ignore venv --savepath requirements2.txt

# dev dependencies
declare -a dev_dependencies=("pipreqs==0.4.13" "flake8==6.0.0" "pytest==7.3.1")

# diff the two requirements files
diff --changed-group-format='%<' --unchanged-group-format='' requirements.txt requirements2.txt > temp_requirements.txt

# filter out the dev dependencies
for dep in "${dev_dependencies[@]}"
do
  grep -v "$dep" temp_requirements.txt > surplus_requirements.txt
  cp surplus_requirements.txt temp_requirements.txt
done

# count total surplus dependencies
surplus_count=$(wc -l < surplus_requirements.txt)
echo "Total number of surplus dependencies in the project: $surplus_count"

echo "Surplus dependencies:"
cat surplus_requirements.txt

# cleanup
rm requirements2.txt
rm temp_requirements.txt
rm surplus_requirements.txt

if [ $surplus_count -gt 0 ]
then
  echo "Error: Surplus dependencies found. If any of these are dev dependencies, add them to the exclusions list in the dev_dependencies array of this script." >&2
  exit 1
fi
