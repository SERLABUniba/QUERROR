import os
import csv
import requests
import time
#import json
from dotenv import load_dotenv
from fontTools.misc.psOperators import ps_integer
from pycparser.c_ast import While

#from github import Github

# Authentication is defined via GitHub.Auth
#from github import Auth

""" Load environment variables from .env file """
load_dotenv()  # loads variables from .env file into environment
token = os.environ.get('GITHUB_TOKEN')
# print(token)

# GitHub API headers
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Function to get the commit SHA based on repo details, commit message, and file path
"""def get_commit_sha(owner, repo, filename, commit_message_query):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "path": filename,  # Search for commits affecting this file
        "q": commit_message_query  # Search for the specific commit message
    }

    # Print the URL for debugging
    print(f"URL: {url}")

    print(f"Params: {params}")

    # Make the GET request to the GitHub API
    response = requests.get(url, headers=headers, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            if commit_message_query in commit["commit"]["message"]:
                return commit["sha"]
        return None  # If no commit found
    else:
        print(f"Failed to retrieve commits for {owner}/{repo}: {response.status_code}")
        return None"""

def normalize_commit_message(message):
    """
    Normalize a commit message by removing extra spaces and line breaks for better comparison.
    :param message: The commit message
    :return: The normalized message
    """
    # If there is a non-english character in the message, it will be removed
    message = message.encode('ascii', 'ignore').decode('ascii')
    return " ".join(message.split()).strip()  # Remove excess whitespace and line breaks

def handle_rate_limit(response):
    """
    Handles GitHub API rate limiting.
    If the rate limit is reached, it waits until the reset time.
    :param response: The response object from the GitHub API request
    """
    rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
    rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time()))

    if rate_limit_remaining == 0:
        reset_time = rate_limit_reset - time.time()
        if reset_time > 0:
            print(f"Rate limit reached. Waiting for {int(reset_time)} seconds...")
            time.sleep(reset_time)
        else:
            print("Rate limit reset time has passed, retrying immediately.")

def get_commit_sha_by_message(owner, repo, commit_message, token):
    """
    Get the commit sha by commit message
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :param commit_message: the commit message
    :param token: GitHub access token
    :return: the commit sha
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    # To implement pagination
    page = 1
    per_page = 1000  # GitHub allows up to 100 commits per page

    # Normalize the search commit message
    normalized_commit_message = normalize_commit_message(commit_message)

    # Print the URL for debugging
    # print(f"URL: {url}")
    # Print the parameters for debugging
    # print(f"Parameters: page={page}, per_page={per_page}")
    # Print the token for debugging
    # print(f"Token: {token}")

    while True:
        # Add pagination parameters to the request
        params = {
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, headers={'Authorization': f'token {token}'}, params=params)

        # Handle rate limiting
        handle_rate_limit(response)

        if response.status_code == 200:
            commits_data = response.json()

            # If no commits are returned, stop searching
            if not commits_data:
                print(f"Commit message not found after searching {page - 1} pages.")
                return None

            #print(f"commits_data: {commits_data}")

            # Search through the current page's commits for the desired commit message
            for c_data in commits_data:
                # print(f"c_data Commit: {c_data['commit']['message']}")
                # print(f"Commit Message: {commit_message}")
                # print('GIT: ',c_data['commit']['message'].lower().strip().replace(" ", "").replace("\n","")[:100])
                # print('TO MATCH: ',commit_message.lower().strip().replace(" ", "").replace("\n","")[:100])
                # Compare the first 100 characters of the commit message with the first 100 characters of the desired commit message
                # if c_data['commit']['message'][:100].lower().strip().replace(" ", "") == commit_message.lower().strip().replace(" ", "")[:100]:
                # if commit_message.lower().strip().replace(" ", "") == c_data['commit']['message'].lower().strip().replace(" ", ""):
                """if "12421" in c_data['commit']['message']:
                    # Convert c_data['commit']['message'] to string
                    qstr = str(c_data['commit']['message'])
                    print(qstr)
                    print(commit_message)"""

                """qstr = c_data['commit']['message']"""

                normalized_github_message = normalize_commit_message(c_data['commit']['message'])

                # if str(c_data['commit']['message']) == str(commit_message):
                # if commit_message in c_data['commit']['message']:
                if normalized_commit_message in normalized_github_message:
                    #print(f"Commit SHA: {c_data['sha']}")
                    #print(f"Commit message: {c_data['commit']['message']}")
                    #return c_data['sha']
                    return c_data['html_url']

            # If no match found, fetch the next page
            page += 1
        else:
            print(f"Failed to fetch commits for {owner}/{repo} (Status code: {response.status_code})")
            return None

def main():
    """
    Main function to fetch UUID from GitHub API and save it to a CSV file.
    :return:
    """

    # Read data from qdata.csv and get the commit SHA for each row
    input_csv = "../DATA/qdata.csv"  # Replace with your input CSV file
    output_csv = "../DATA/qdata_sha_url.csv"  # Output CSV file

    with open(input_csv, mode="r", newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['commit_sha_url']  # Add a new column for the SHA

        with open(output_csv, mode="w", newline='', encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Loop through each row in the input CSV
            for row in reader:
                owner = row['Owner']
                repo = row['Repo Name']
                filename = row['Filename']
                commit_message = row['Commit Message']

                #commit_sha = get_commit_sha_by_message(owner, repo, commit_message, token)
                #print('SHA: ',commit_sha)
                #exit(0)
                commit_sha_url = get_commit_sha_by_message(owner, repo, commit_message, token)
                print('HTML Url: ', commit_sha_url)

                # Append the SHA to the row and write to the new CSV
                #row['commit_sha'] = commit_sha if commit_sha else 'Not Found'
                row['commit_sha_url'] = commit_sha_url if commit_sha_url else 'Not Found'
                writer.writerow(row)

    print(f"Output written to {output_csv}")

if __name__ == "__main__":
    main()
