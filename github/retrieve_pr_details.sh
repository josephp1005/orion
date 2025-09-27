#!/bin/bash
# Create/clear the output file
> json/body.json

owner=$1
repo=$2

# Loop through pages
page=1
while [ $page -lt 5 ]; do
    echo "Fetching page $page..."
    
    # Get the page
    response=$(curl -s -L "https://api.github.com/repos/${owner}/${repo}/pulls?state=all&per_page=100&page=$page")
    
    # Check if we got any results
    count=$(echo "$response" | jq length)
    
    if [ "$count" -eq 0 ]; then
        echo "No more results. Done!"
        break
    fi
    
    # Extract bodies and append to file
    echo "$response" | jq '.[].body' >> json/body.json
    
    echo "Got $count PRs from page $page"
    page=$((page + 1))
    
    # Optional: add a small delay to be nice to the API
    sleep 1
done

echo "Formatting the collected PR bodies..."
python3 pretty_print_body.py --convert json/body.json json/body.txt

echo "Total PRs collected: $(wc -l < json/body.json)"

echo "Fetching diff files for the PRs..."

# Create diffs directory if it doesn't exist
mkdir -p json/diffs

# Extract the PR numbers from the refined JSON file
pr_numbers=$(jq -r '.[].pr_number' json/refinedev_refine_refined_pr_info.json)

count=0
for pr_number in $pr_numbers; do
    echo "Downloading diff for PR #$pr_number..."

    curl -L \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3.diff" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/${owner}/${repo}/pulls/${pr_number}" \
    -o "json/diffs/${pr_number}.diff"

    count=$((count + 1))
    echo "Downloaded $count diffs"

    # Optional: add a small delay to be nice to the API
    sleep 0.5
done

echo "Finished downloading $count diff files to json/diffs/ directory"