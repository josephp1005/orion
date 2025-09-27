import requests
import json
import os
import sys
from typing import List, Dict, Any
import subprocess

class GitHubPRFetcher:
    def __init__(self, token: str = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PR-Fetcher"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "open", 
                         per_page: int = 30, page: int = 1) -> List[Dict[Any, Any]]:
        """
        Fetch pull requests from a GitHub repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state ('open', 'closed', 'all')
            per_page: Number of results per page (max 100)
            page: Page number
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {
            "state": state,
            "per_page": per_page,
            "page": page,
            "sort": "created",
            "direction": "desc"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching PRs: {e}")
            return []
    
    def get_all_pull_requests(self, owner: str, repo: str, state: str = "open") -> List[Dict[Any, Any]]:
        """Fetch all pull requests across multiple pages"""
        all_prs = []
        page = 1
        
        while True:
            prs = self.get_pull_requests(owner, repo, state, per_page=100, page=page)
            if not prs:
                break
            
            all_prs.extend(prs)
            page += 1
            
            # GitHub API returns fewer results when we've reached the end
            if len(prs) < 100:
                break
        
        return all_prs
    
    def save_to_file(self, data: List[Dict[Any, Any]], filename: str):
        """Save PR data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} pull requests to {filename}")
    
    def get_pr_summary(self, prs: List[Dict[Any, Any]]) -> Dict[str, Any]:
        """Get summary statistics of pull requests"""
        if not prs:
            return {}
        
        states = {}
        authors = {}
        labels = {}
        
        for pr in prs:
            # Count states
            state = pr.get('state', 'unknown')
            states[state] = states.get(state, 0) + 1
            
            # Count authors
            author = pr.get('user', {}).get('login', 'unknown')
            authors[author] = authors.get(author, 0) + 1
            
            # Count labels
            for label in pr.get('labels', []):
                label_name = label.get('name', 'unknown')
                labels[label_name] = labels.get(label_name, 0) + 1
        
        return {
            "total_prs": len(prs),
            "states": states,
            "top_authors": dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_labels": dict(sorted(labels.items(), key=lambda x: x[1], reverse=True)[:10])
        }

def main():
    # Get GitHub token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    
    # Get repository name from command line argument
    if len(sys.argv) != 2:
        print("Usage: python3 fetch_prs.py <owner/repo>")
        print("Example: python3 fetch_prs.py refinedev/refine")
        sys.exit(1)
    
    repo_name = sys.argv[1].strip()
    
    # Validate repository name format
    if '/' not in repo_name or len(repo_name.split('/')) != 2:
        print("Error: Repository name must be in format 'owner/repo'")
        print("Example: refinedev/refine")
        sys.exit(1)
    
    if not token:
        print("Warning: No GITHUB_TOKEN found. API rate limits will be lower.")
    
    fetcher = GitHubPRFetcher(token)

    owner = repo_name.split('/')[0]
    repo = repo_name.split('/')[1]
    
    print(f"Fetching pull requests from {owner}/{repo}...")
    
    # Get open PRs
    open_prs = fetcher.get_pull_requests(owner, repo, state="open", per_page=50)
    print(f"Found {len(open_prs)} open pull requests")
    
    # Get closed PRs (limited to avoid rate limits)
    closed_prs = fetcher.get_pull_requests(owner, repo, state="closed", per_page=50)
    print(f"Found {len(closed_prs)} recent closed pull requests")
    
    # Combine and save
    all_prs = open_prs + closed_prs
    
    # Save to file with repo name in filename
    filename = f"json/{owner}_{repo}_pull_requests.json"
    fetcher.save_to_file(all_prs, filename)
    
    subprocess.run(["python3", "analyze_prs.py", filename], shell=False)
    subprocess.run(["./retrieve_pr_details.sh", owner, repo], shell=False)

    #############################################################################
    #############################################################################
    ################ Implement Logic to Save Data to Database ################
    #############################################################################
    #############################################################################

    for file in os.listdir('json/diffs'):
        os.remove(os.path.join('json/diffs', file))

    for file in os.listdir('json'):
        os.remove(os.path.join('json', file))

if __name__ == "__main__":
    main()
