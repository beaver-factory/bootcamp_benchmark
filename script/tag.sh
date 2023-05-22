#!/bin/bash
echo -e "\n"

tag_version=$1

# Check if the user provided a valid tag version
if [ "$tag_version" != "major" ] && [ "$tag_version" != "minor" ] && [ "$tag_version" != "patch" ]; then
    echo "❌ Invalid tag version. Please provide either 'major', 'minor', or 'patch'."
    exit 0
fi

current_branch=$(git symbolic-ref --short HEAD)

# Check if the current branch is not 'main'
if [ "$current_branch" != "main" ]; then
    echo "❌ Current branch is not 'main'. You're on '$current_branch' branch."
    exit 1
fi

echo -e "✅ Current branch is  'main'.\n"

# # Check if main is up-to-date with remote

echo -e "• Checking if 'main' is up-to-date with remote:\n"

git fetch origin main

if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ]; then
    echo "❌ 'main' is not up-to-date with remote. Please pull the latest changes."
    exit 1
fi

# Get the most recent tag
recent_tag=$(git describe --tags `git rev-list --tags --max-count=1` 2>/dev/null)

new_tag=""

if [ -z "$recent_tag" ]; then
    # If no tags found, create the first ever tag
    echo -e "👀 No tags found in the repository.\n"
    new_tag="v0.1.0"
    echo -e "✅ Creating first tag: $new_tag\n"
elif [ "$tag_version" == "patch" ]; then
    echo -e "• Applying PATCH update:\n"

    version_parts=(${recent_tag//./ })
    ((version_parts[2]++))
    new_tag="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"

    echo -e "\t $recent_tag → $new_tag \n"
elif [ "$tag_version" == "minor" ]; then
    echo -e "• Applying MINOR update:\n"

    version_parts=(${recent_tag//./ })
    ((version_parts[1]++))
    version_parts[2]=0
    new_tag="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"

    echo -e "\t $recent_tag → $new_tag \n"
elif [ "$tag_version" == "major" ]; then
    echo -e "• Applying MAJOR update:\n"

    version_parts=(${recent_tag//v/ }) # Remove 'v' from version
    version_numbers=(${version_parts[0]//./ }) # Split version numbers

    ((version_numbers[0]++))
    version_numbers[1]=0
    version_numbers[2]=0
    new_tag="v${version_numbers[0]}.${version_numbers[1]}.${version_numbers[2]}"

    echo -e "\t $recent_tag → $new_tag \n"
else
    echo "❌ Tag version is not 'patch', 'minor' or 'major'. No update applied."
    exit 0
fi

echo -e "❓ Type 'YEE-HAW' to publish new tag:\n"
read user_input

# Check the user's input
if [ "$user_input" == "YEE-HAW" ]; then
    echo -e "\n"
    # publish new tag
    git tag -a $new_tag -m "auto-generated tag"
    git push origin $new_tag
    echo "✅ published new tag: $new_tag"
else
    echo "❌ Exiting..."
    exit 1
fi


echo -e "\n"
