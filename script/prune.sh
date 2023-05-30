#!/bin/bash

# build new reqs from current project
pipreqs ./ --ignore venv --savepath requirements2.txt

# diff the two requirements files
diff --changed-group-format='%<' --unchanged-group-format='' requirements.txt requirements2.txt > surplus_requirements.txt

# count total surplus dependencies
surplus_count=$(wc -l < surplus_requirements.txt)
echo "Total number of surplus dependencies in the project: $surplus_count"

echo "Surplus dependencies:"
cat surplus_requirements.txt

# cleanup
rm requirements2.txt
rm surplus_requirements.txt

if [ $surplus_count -gt 0 ]
then
  echo "Error: Surplus dependencies found." >&2
  exit 1
fi
