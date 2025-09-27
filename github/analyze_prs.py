import json
from datetime import datetime
from typing import List, Dict, Any
import sys

def load_pr_data(filename: str) -> List[Dict[Any, Any]]:
    """Load PR data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_pull_requests(prs: List[Dict[Any, Any]]):
    """Analyze pull request data"""
    print(f"Total Pull Requests: {len(prs)}")
    print("-" * 50)
    
    # Analyze states
    states = {}
    for pr in prs:
        state = pr.get('state', 'unknown')
        states[state] = states.get(state, 0) + 1
    
    print("States:")
    for state, count in states.items():
        print(f"  {state}: {count}")
    
    # Analyze authors
    authors = {}
    for pr in prs:
        author = pr.get('user', {}).get('login', 'unknown')
        authors[author] = authors.get(author, 0) + 1
    
    print(f"\nTop Authors:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {author}: {count} PRs")
    
    # Analyze labels
    labels = {}
    for pr in prs:
        for label in pr.get('labels', []):
            label_name = label.get('name', 'unknown')
            labels[label_name] = labels.get(label_name, 0) + 1
    
    if labels:
        print(f"\nTop Labels:")
        for label, count in sorted(labels.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {label}: {count}")
    
    # Recent PRs
    print(f"\nRecent Pull Requests:")
    for pr in prs[:5]:
        title = pr.get('title', 'No title')[:60]
        author = pr.get('user', {}).get('login', 'unknown')
        state = pr.get('state', 'unknown')
        created = pr.get('created_at', '')[:10]  # Just the date part
        print(f"  #{pr.get('number', '?')} - {title}... ({author}, {state}, {created})")

def extract_commit_info(prs: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
    """Extract commit-related information from PRs"""
    commit_info = []
    
    for pr in prs:
        info = {
            'pr_number': pr.get('number'),
            'title': pr.get('title'),
            'author': pr.get('user', {}).get('login'),
            'head_sha': pr.get('head', {}).get('sha'),
            'base_sha': pr.get('base', {}).get('sha'),
            'head_ref': pr.get('head', {}).get('ref'),
            'base_ref': pr.get('base', {}).get('ref'),
            'merge_commit_sha': pr.get('merge_commit_sha'),
            'state': pr.get('state'),
            'created_at': pr.get('created_at'),
            'updated_at': pr.get('updated_at'),
            'merged_at': pr.get('merged_at')
        }
        commit_info.append(info)
    
    return commit_info

if __name__ == "__main__":
    # Load and analyze your existing PR data

    if len(sys.argv) != 2:
        print("Usage: python3 analyze_prs.py <path_to_pr_json>")
        print("Example: python3 analyze_prs.py /Users/testuser/hack-gt.py")
        sys.exit(1)

    pr_json_path = sys.argv[1].strip()
    owner = pr_json_path.split('/')[-1].split('_')[0]
    repo = pr_json_path.split('/')[-1].split('_')[1]

    prs = load_pr_data(pr_json_path)
    analyze_pull_requests(prs)
    
    # Extract commit information
    commit_info = extract_commit_info(prs)
    
    # Save commit info
    with open(f"json/{owner}_{repo}_refined_pr_info.json", 'w') as f:
        json.dump(commit_info, f, indent=2)
    
    print(f"\nExtracted commit info for {len(commit_info)} PRs")
    