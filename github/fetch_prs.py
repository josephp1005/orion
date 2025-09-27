import requests
import json
import os
import sys
from typing import List, Dict, Any
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dense_embeddings import git_pr_pipeline

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
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls?per_page={per_page}&page={page}&state=all"
        
        try:
            response = requests.get(url, headers=self.headers)
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
            print("H PAGE", page)
            prs = self.get_pull_requests(owner, repo, state, per_page=50, page=page)
            if not prs:
                break
            
            all_prs.extend(prs)
            page += 1
            
            # GitHub API returns fewer results when we've reached the end
            
            if len(prs) < 50:
                break

            if page > 3:
                break
        
        return all_prs
    
    def get_new_pull_requests(self, owner, repo, token, json_filename, refined_filename, state) -> List[Dict[Any, Any]]:
        """Fetch all pull requests across multiple pages"""
        new_prs = []
        with open(json_filename, 'r') as f:
            existing_prs = json.load(f)
            print("Number of existing PRs:", len(existing_prs))
            print(type(existing_prs))

        existing_pr_numbers = set(existing_prs[i]["number"] for i in range(len(existing_prs)))
        print(existing_pr_numbers)

        url = f"{self.base_url}/repos/{owner}/{repo}/pulls?&page=1&per_page=20&state=all&sort=created&direction=desc"
        response = requests.get(url, headers=self.headers)

        recent_prs = response.json()
        for pr in recent_prs:
            if pr["number"] not in existing_pr_numbers:
                print("New PR found:", pr["number"], pr["title"])
                new_prs.append(pr)

        if len(new_prs) == 0:
            print("No new PRs found.")
            return

        new_json_filename = f"json/new_{owner}_{repo}_pull_requests.json"
        new_refined_json_filename = f"json/new_{owner}_{repo}_refined_pr_info.json"
        with open(new_json_filename, 'w') as f:
            json.dump(new_prs, f, indent=2)

        subprocess.run(["python3", "analyze_prs.py", new_json_filename, "n"], shell=False)

        with open(new_refined_json_filename, 'r') as f:
            new_pr_info = json.load(f)

        for i in range(len(new_pr_info)):
            result = subprocess.run([
                                        "curl",
                                        "-H", "Accept: application/vnd.github+json",
                                        "-H", f"Authorization: Bearer {token}",
                                        "-H", "X-GitHub-Api-Version: 2022-11-28",
                                        f"https://api.github.com/repos/{owner}/{repo}/pulls/{new_pr_info[i]['pr_number']}",
                                    ], capture_output=True, text=True)
            pr_specific_info = json.loads(result.stdout)
            pr_body = pr_specific_info["body"]
            new_pr_info[i]['pr_body'] = pr_body

            pr_number = new_pr_info[i]["pr_number"]
            result = subprocess.run([
                    "curl",
                    "-L",
                    "-H", f"Authorization: Bearer {token}",
                    "-H", "Accept: application/vnd.github.v3.diff",
                    "-H", "X-GitHub-Api-Version: 2022-11-28",
                    f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
                ], capture_output=True, text=True)
            diff = result.stdout
            new_pr_info[i]["diff"] = f'"""{diff}"""'

        with open(new_refined_json_filename, 'w') as f:
            json.dump(new_pr_info, f, indent=2)

        with open(refined_filename, 'r') as f:
            refined_existing_prs = json.load(f)

        refined_existing_prs.extend(new_pr_info)
        with open(refined_filename, 'w') as f:
            json.dump(refined_existing_prs, f, indent=2)

    
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
    
    def add_pr_body_to_json(self, refined_json_filename: str, token, owner, repo):
        """Add PR body descriptions to the refined PR info JSON file"""
        with open(refined_json_filename, 'r') as f:
            refined_pr_info = json.load(f)

        for i in range(len(refined_pr_info)):
            result = subprocess.run([
                                        "curl",
                                        "-H", "Accept: application/vnd.github+json",
                                        "-H", f"Authorization: Bearer {token}",
                                        "-H", "X-GitHub-Api-Version: 2022-11-28",
                                        f"https://api.github.com/repos/{owner}/{repo}/pulls/{refined_pr_info[i]['pr_number']}",
                                    ], capture_output=True, text=True)
            pr_specific_info = json.loads(result.stdout)
            print(type(pr_specific_info))
            pr_body = pr_specific_info["body"]
            refined_pr_info[i]['pr_body'] = pr_body

        with open(refined_json_filename, 'w') as f:
            json.dump(refined_pr_info, f, indent=2)

    def add_diff_to_pr_info(self, owner, repo, refined_json_filename, token):
        """
        Add diff information to each PR dictionary in the JSON file.
        """
        with open(refined_json_filename, 'r') as f:
            refined_pr_info = json.load(f)

        for i in range(len(refined_pr_info)):
            pr_number = refined_pr_info[i]["pr_number"]
            result = subprocess.run([
                    "curl",
                    "-L",
                    "-H", f"Authorization: Bearer {token}",
                    "-H", "Accept: application/vnd.github.v3.diff",
                    "-H", "X-GitHub-Api-Version: 2022-11-28",
                    f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
                ], capture_output=True, text=True)
            diff = result.stdout
            refined_pr_info[i]["diff"] = f'"""{diff}"""'
        
        with open(refined_json_filename, 'w') as f:
            json.dump(refined_pr_info, f, indent=2)

def main():
    # Get GitHub token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    
    # Get repository name from command line argument
    if len(sys.argv) < 2:
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

    filename = f"json/{owner}_{repo}_pull_requests.json"
    refined_json_filename = f"json/{owner}_{repo}_refined_pr_info.json"

    if len(sys.argv) == 2:
        all_prs = fetcher.get_all_pull_requests(owner, repo, state="all")
        print(f"Found {len(all_prs)} total pull requests")
        
        # Save to file with repo name in filename
        fetcher.save_to_file(all_prs, filename)
        subprocess.run(["python3", "analyze_prs.py", filename], shell=False)
        fetcher.add_pr_body_to_json(refined_json_filename, token, owner, repo)
        fetcher.add_diff_to_pr_info(owner, repo, refined_json_filename, token)
    else:
        fetcher.get_new_pull_requests(owner, repo, token, filename, refined_json_filename, state="all")

    #############################################################################
    #############################################################################
    ################ Implement Logic to Save Data to Database ################
    #############################################################################
    #############################################################################

    for file in os.listdir('json/diffs'):
        os.remove(os.path.join('json/diffs', file))

    git_pr_pipeline()

if __name__ == "__main__":
    main()
