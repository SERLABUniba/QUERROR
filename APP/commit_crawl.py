# import io
import os
import csv
import datetime
import sys
import requests
from dotenv import load_dotenv
from github import Github
# from docx import Document
# import PyPDF2


# Authentication is defined via GitHub.Auth
from github import Auth

""" Load environment variables from .env file """
load_dotenv()  # loads variables from .env file into environment
access_token = os.environ.get('ACCESS_TOKEN')

""" GitHub Authentication using an access token - PyGitHub """
auth = Auth.Token(access_token)

# start python session and create object
# session = requests.Session()
# session.headers.update({'Authorization': f"token {access_token}"})


def get_repo_names(g):
    """
    Get the names of the repositories from GitHub search
    :param g:
    :return: list of repo names
    """
    repos = []
    quantum_programs = []

    # Branches to check
    branches = ['main', 'master']

    for repo in g.search_repositories(query="quantum OR dwave OR cirq OR qml OR qiskit stars:>50 pushed:>2023-01-01",
                                      sort="stars", order="desc"):
        repos.append(repo.name)
        # print(repo.name)
        repo_name = repo.name
        repo_owner = repo.owner.login

        # Traverse in the branches to check if the repos has a readme file
        for branch_name in branches:
            try:
                branch = repo.get_branch(branch_name)
            except Exception as e:
                print(f"Branch '{branch_name}' does not exist in repository '{repo_name}'. "
                      f"Checking the next branch or repository.")
                continue
            tree = repo.get_git_tree(branch.commit.sha, recursive=True)

            # Search for files in the repository that start with 'readme'(case-insensitive)
            readme_files = [file for file in tree.tree if file.path.lower().startswith('readme')]

            if not readme_files:
                print(f"No files starting with 'readme' found in branch '{branch_name}' of repository '{repo_name}'. "
                      f"Checking the next branch or repository.")
                continue
            # print(f"Read Me Files: {readme_files}")  # Print the list of readme_files
            for readme_file in readme_files:
                if readme_file.type == 'tree':  # Check if the item is a directory
                    # print(f"Directory: {readme_file.path}")
                    """# Go to the directory and get the readme file if exists
                    subdir_tree = repo.get_git_tree(readme_file.sha, recursive=True)
                    subdir_readme_files = [file for file in subdir_tree.tree if file.path.lower().startswith('readme')]
                    print(subdir_readme_files)
                    if not subdir_readme_files:
                        print(
                            f"No files starting with 'readme' found inside the directory '{readme_file.path}' "
                            f"in branch '{branch_name}' of repository '{repo_name}'.")
                    else:
                        for subdir_readme_file in subdir_readme_files:
                            # Process the files inside the directory
                            subdir_content = (repo.get_contents(subdir_readme_file.path, ref=branch.commit.sha).
                                              decoded_content.decode())
                            print(f"Found file starting with 'readme' inside the directory '"
                                  f"{readme_file.path}': "f"'{subdir_readme_file.path}'")
                            if 'quantum' in subdir_content.lower() or 'dwave' in subdir_content.lower():
                                # Get the URL of the readme file
                                subdir_readme_url = (f"https://github.com/{repo_owner}/{repo_name}"
                                                     f"/blob/"f"{branch_name}/{subdir_readme_file.path}")
                                print(f"URL of the file: {subdir_readme_url}")
                                # Add the quantum program to the list
                                quantum_programs.append({
                                    "name": repo.name,
                                    "owner": repo.owner.login,
                                    "description": repo.description,
                                    "html_url": repo.html_url,
                                    "readme_url": subdir_readme_url
                                })
                            else:
                                print(f"File '{subdir_readme_file.path}' in branch '{branch_name}' of repository "
                                      f"DOES NOT contain the word 'quantum' or 'dwave' / or the readme is "
                                      f"non-latin language.")"""
                    # If directory then go to next item in readme_files
                    continue
                else:
                    # print("readme file: ", readme_file)
                    # print("readme file path: ", readme_file.path)
                    # print(repo.get_contents(readme_file.path, ref=branch.commit.sha))

                    # Check if the readme file contains a '/' in the path
                    # If it does, extract the file name by splitting
                    if '/' in readme_file.path:
                        file_name = readme_file.path.split('/')[-1]
                        # print(f"File name extracted from path '{readme_file.path}': {file_name}")
                        # Check if the file name starts with 'readme' and ends with '.md' or '.rst' or '.txt'
                        if (file_name.lower().startswith('readme') and
                                (file_name.lower().endswith('.md') or file_name.lower().endswith('.rst')
                                 or file_name.lower().endswith('.txt'))):
                            # print("IN THIS PART")
                            # print(f"File name extracted from path '{readme_file.path}': {file_name}")
                            content = repo.get_contents(readme_file.path,
                                                        ref=branch.commit.sha).decoded_content.decode()

                            if 'quantum' in content.lower() or 'dwave' in content.lower():
                                # Get the URL of the readme file
                                readme_url = (f"https://github.com/{repo_owner}/{repo_name}/blob/"
                                              f"{branch_name}/{readme_file.path}")
                                print(f"URL of the file: {readme_url}")

                                # Add the quantum program to the list
                                quantum_programs.append({
                                    "name": repo.name,
                                    "owner": repo.owner.login,
                                    "description": repo.description,
                                    "html_url": repo.html_url,
                                    "readme_url": readme_url
                                })
                        else:
                            print(f"File '{readme_file.path}' DOES NOT start with readme.")
                    else:
                        # Readme file does not contain a '/' and exists with name starting with 'readme'
                        # print(f"File '{readme_file.path}' in branch '{branch_name}' of repository ")
                        # Check what does the file ends with.
                        # If it ends with .md or .rst or .txt then do as below
                        # print("IN THIS PART: ", readme_file.path)
                        if (readme_file.path.endswith('.md') or readme_file.path.endswith('.rst') or
                                readme_file.path.endswith('.txt')):
                            # Get the content of the file
                            content = (repo.get_contents(readme_file.path, ref=branch.commit.sha).
                                       decoded_content.decode())
                            # Check if the content contains the word 'quantum' or 'dwave' (case-insensitive)
                            if 'quantum' in content.lower() or 'dwave' in content.lower():
                                # print(f"File '{readme_file.path}' in branch '{branch_name}' of repository "
                                #      f"'{repo_name}' contains the word 'quantum'.")
                                # Get the URL of the readme file
                                readme_url = (f"https://github.com/{repo_owner}/{repo_name}/blob/"
                                              f"{branch_name}/{readme_file.path}")
                                print(f"URL of the file: {readme_url}")

                                # Add the quantum program to the list
                                quantum_programs.append({
                                    "name": repo.name,
                                    "owner": repo.owner.login,
                                    "description": repo.description,
                                    "html_url": repo.html_url,
                                    "readme_url": readme_url
                                })
                            else:
                                print(f"File '{readme_file.path}' in branch '{branch_name}' of repository "
                                      f"DOES NOT contain the word 'quantum' or 'dwave' / or the readme is "
                                      f"non-latin language.")
                        """elif readme_file.path.endswith('.docx'):
                            # Get the content of the file
                            docx_file_content = repo.get_contents(readme_file.path).decoded_content
                            doc = Document(io.BytesIO(docx_file_content))
                            content = " ".join([paragraph.text for paragraph in doc.paragraphs])
                            # Check if the content contains the word 'quantum' or 'dwave' (case-insensitive)
                            if 'quantum' in content.lower() or 'dwave' in content.lower():
                                # print(f"File '{readme_file.path}' in branch '{branch_name}' of repository "
                                #      f"'{repo_name}' contains the word 'quantum'.")
                                # Get the URL of the readme file
                                readme_url = (f"https://github.com/{repo_owner}/{repo_name}/blob/"
                                              f"{branch_name}/{readme_file.path}")
                                print(f"URL of the file: {readme_url}")

                                # Add the quantum program to the list
                                quantum_programs.append({
                                    "name": repo.name,
                                    "owner": repo.owner.login,
                                    "description": repo.description,
                                    "html_url": repo.html_url,
                                    "readme_url": readme_url
                                })
                        elif readme_file.path.endswith('.pdf'):
                            # Get the content of the file
                            pdf_file_content = (repo.get_contents(readme_file.path, ref=branch.commit.sha).contents.
                                                decoded_content)
                            pdf = PyPDF2.PdfFileReader(io.BytesIO(pdf_file_content))
                            num_pages = pdf.getNumPages()
                            # Check for the existence of quantum in the content
                            for page_num in range(num_pages):
                                page = pdf.getPage(page_num)
                                text = page.extractText()
                                if 'quantum' in text.lower() or 'dwave' in text.lower():
                                    readme_url = (f"https://github.com/{repo_owner}/{repo_name}/blob/"
                                                  f"{branch_name}/{readme_file.path}")
                                    print(f"URL of the file: {readme_url}")
                                    # Add the quantum program to the list
                                    quantum_programs.append({
                                        "name": repo.name,
                                        "owner": repo.owner.login,
                                        "description": repo.description,
                                        "html_url": repo.html_url,
                                        "readme_url": readme_url
                                    })"""

    print(len(repos))
    print(len(quantum_programs))
    return quantum_programs


def search_github_repositories(query, num, max_results):
    """
    Search for repositories on GitHub based on the given query and number of results.
    :param query:
    :param num:
    :param max_results:
    :return: json response
    """
    url = "https://api.github.com/search/repositories"
    # params = {
    #     "q": f"{query} language:{language}",
    #     "sort": "stars",
    #     "order": "desc",
    #     "per_page": max_results
    # }

    # Parameters to pass to the API
    params = {
        # more than 30 stars
        "q": f"{query} stars:>={num}",
        # "q": f"{query}",
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }

    # print(f"ACCESS_TOKEN: {access_token}")

    response = requests.get(url, params=params, headers={'Authorization': f'token {access_token}'})
    # print(f"Response: {response}")

    if response.status_code == 200:
        print("Repositories fetched successfully !!")
        # Printing the number of repos extracted for testing purpose
        var = response.json()["items"]
        count_dicts = len([d for d in var if isinstance(d, dict)])
        print(f"Count of repositories: {count_dicts}")
        # End test block
        return response.json()["items"]
    else:
        print(f"Error: Unable to fetch repositories (Status code: {response.status_code})")
        return []


def extract_quantum_programs(repositories):
    """
    Extracts quantum programs from the given list of repositories.
    :param repositories:
    :return: list of quantum programs
    """
    # print(f"Repositories: {repositories}")
    quantum_programs = []
    for repo in repositories:
        repo_name = repo["full_name"]
        # print(f"Repository: {repo_name}")
        code_url = f"https://api.github.com/repos/{repo_name}/contents"

        branch = ["master", "main"]
        # Check if the repo has any files starting with README
        # Check in both master and main
        response = requests.get(code_url, headers={'Authorization': f'token {access_token}'})
        print(f"Code URL: {code_url}")
        if response.status_code == 200:
            contents = response.json()
            # Get the list of readme files in the repo based on if they start with README but case-insensitive
            readme_files = [content["name"] for content in contents if content["name"].lower().startswith("readme")]
            # print(f"Readme files: {readme_files}")

            # If there are no readme files then skip
            if not readme_files:
                continue
            else:
                for br in branch:
                    readme_url = f"https://raw.githubusercontent.com/{repo_name}/{br}/{readme_files[0]}"
                    # print(f"Readme URL: {readme_url}")
                    readme_response = requests.get(readme_url, headers={'Authorization': f'token {access_token}'})
                    if readme_response.status_code == 200:
                        readme_content = readme_response.text
                        if ("quantum" in readme_content.lower() or "dwave" in readme_content.lower()
                                or "qiskit" in readme_content.lower()):
                            # if True:
                            # print(f"Readme content: {readme_content}")
                            # print(f"README URL: {readme_url}")
                            quantum_programs.append({
                                "name": repo["name"],
                                "owner": repo["owner"]["login"],
                                "description": repo["description"],
                                "html_url": repo["html_url"],
                                "readme_url": readme_url
                            })

    return quantum_programs


def verify_list_of_dicts_num(var, num):
    """
    Verify if the list of dictionaries contains the specified number of fields
    :param var: the variable to be verified
    :param num: the number of fields
    :return: boolean
    """
    if isinstance(var, list):
        for element in var:
            if not isinstance(element, dict):
                return False
            if len(element) != num:
                return False
        return True
    return False


def verify_list_of_dicts_key(var, key_name):
    """
    Verify if the list of dictionaries contains the specified key
    :param var: the variable to be verified
    :param key_name: if the key name does not exist then return False
    :return: boolean
    """
    if isinstance(var, list):
        for element in var:
            if not isinstance(element, dict):
                return False
            if key_name not in element:
                return False
        return True
    return False


def save_to_csv(data, filename):
    """
    Save the data to a CSV file
    :param data: the data to be saved
    :param filename: the name of the file
    :return: None
    """
    # Check if the file with the same name already exists then delete the file
    if os.path.exists(filename):
        # strip the extension
        fn = os.path.splitext(filename)[0]
        # Rename the file to backup(filename) with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        os.rename(filename, f"{fn}_{timestamp}_bak.csv")

    # check if the data, which is a list of dictionaries, contains five fields
    if verify_list_of_dicts_key(data, "readme_url"):
        fields = ["name", "owner", "description", "html_url", "readme_url"]
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    elif verify_list_of_dicts_key(data, "changes"):
        # fields = ["repo", "commit_hash", "commit_message", "filename", "changes"]
        fields = ["repo", "commit_message", "filename", "changes"]
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)


def fetch_commit_diff(owner, repo, commit_sha):
    """
    Fetch the commit diff
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :param commit_sha: the commit sha
    :return: None
    """
    # Get the commit diff
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        commit_data = response.json()
        files_changed = commit_data['files']
        # print(f"Files changed: {files_changed}")
        changes = []
        # print(f"Files changed: \n {files_changed}")
        for file_changed in files_changed:
            filename = file_changed['filename']
            # If the patch is empty or invalid assignment, skip it
            # print(f"File: {filename}")
            # print(f"Patch: {file_changed['patch']}")
            if 'patch' not in file_changed or not file_changed['patch']:
                print(f"File: {filename}; No patch available")
                continue
            else:
                patch = file_changed['patch']
                print(f"File: {filename}, Patch: {patch}")
                changes.append((filename, patch))

        return changes
    else:
        print(f"Failed to fetch commit diff for {commit_sha} in {owner}/{repo} (Status code: {response.status_code})")
        return []


def get_commit_sha_by_message(owner, repo, commit_message):
    """
    Get the commit sha by commit message
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :param commit_message: the commit message
    :return: the commit sha
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        commits_data = response.json()
        for commit_data in commits_data:
            if commit_data['commit']['message'] == commit_message:
                print(f"Commit SHA: {commit_data['sha']}")
                print(f"Commit message: {commit_data['commit']['message']}")
                return commit_data['sha']
        return None
    else:
        print(f"Failed to fetch commits for {owner}/{repo} (Status code: {response.status_code})")
        return None


def fetch_commit_messages(owner, repo):
    """
    Fetch the commit messages
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :return: the commit messages
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    # print(f"Commit URL: {url}")  # Debugging url
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        commits_data = response.json()
        commit_messages = [commit['commit']['message'] for commit in commits_data]
        return commit_messages
    else:
        print(f"Failed to fetch commit messages for {owner}/{repo} (Status code: {response.status_code})")
        return []


def fetch_code_changes(owner, repo):
    """
    Fetch the code changes
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :return: the code changes
    """
    # Get the commit messages
    commit_messages = fetch_commit_messages(owner, repo)

    bug_fix_commits = []

    for commit_message in commit_messages:
        if search_bug_fix_terms(commit_message):
            bug_fix_commits.append(commit_message)

    bug_fix_changes = {}
    for commit_message in bug_fix_commits:
        commit_sha = get_commit_sha_by_message(owner, repo, commit_message)
        if commit_sha:
            changes = fetch_commit_diff(owner, repo, commit_sha)
            bug_fix_changes[commit_message] = changes

    return bug_fix_changes


def fetch_pull_requests_and_issues(owner, repo):
    """
    Fetch the pull requests and issues
    :param owner: the owner of the repository
    :param repo: the name of the repository
    :return: the pull requests and issues
    """
    pull_requests = fetch_pull_requests(owner, repo)
    issues = fetch_issues(owner, repo)
    return pull_requests, issues


def process_commit_data(quantum_programs):
    """
    Process the commit data
    :param quantum_programs: the quantum programs
    :return: the commit data
    """
    # Declare a dictionary to store the code diffs.
    # The key is the file and the value is the code diff for that commit.
    code_diff = []

    # From the quantum_programs, extract the owner and repository name for each program
    for program in quantum_programs:
        owner = program["owner"]
        repo = program["name"]
        bug_fix_changes = fetch_code_changes(owner, repo)

        for commit_message, changes in bug_fix_changes.items():
            # print(f"Commit Message: {commit_message}")
            # commit_hash = get_commit_sha_by_message(owner, repo, commit_message)
            for filename, patch in changes:
                # print(f"File: {filename}")
                # print("Changes:")
                # print(patch)
                # code_diff.append({"repo": repo, "commit_hash": commit_hash, "commit_message": commit_message,
                #                  "filename": filename, "changes": patch})
                code_diff.append({"repo": repo, "commit_message": commit_message,
                                  "filename": filename, "changes": patch})
                # code_diff[filename] = patch
                # print("\n")

    print(code_diff)
    return code_diff

#############################
# Start Pull Requests/Issues
#############################


def fetch_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        pulls_data = response.json()
        pull_requests = [(pull['number'], pull['title'], pull['body']) for pull in pulls_data]
        return pull_requests
    else:
        print(f"Failed to fetch pull requests for {owner}/{repo} (Status code: {response.status_code})")
        return []


def fetch_pull_request_commits(owner, repo, pull_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/commits"
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    print(f"Pull Request URL: {url}")  # Debugging url
    if response.status_code == 200:
        commits_data = response.json()
        commit_messages = [commit['commit']['message'] for commit in commits_data]
        return commit_messages
    else:
        print(f"Failed to fetch commit messages for pull request #{pull_number} in {owner}/{repo} "
              f"(Status code: {response.status_code})")
        return []


def fetch_pull_request_code_changes(owner, repo):
    pull_requests = fetch_pull_requests(owner, repo)
    commit_messages = []

    for pull_request in pull_requests:
        pull_number = pull_request[0]
        commit_messages = fetch_pull_request_commits(owner, repo, pull_number)

    bug_fix_commits = []

    for commit_message in commit_messages:
        if search_bug_fix_terms(commit_message):
            bug_fix_commits.append(commit_message)

    pull_bug_fix_changes = {}
    for commit_message in bug_fix_commits:
        commit_sha = get_commit_sha_by_message(owner, repo, commit_message)
        if commit_sha:
            changes = fetch_commit_diff(owner, repo, commit_sha)
            pull_bug_fix_changes[commit_message] = changes

    return pull_bug_fix_changes


def fetch_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        issues_data = response.json()
        issues = [(issue['number'], issue['title'], issue['body']) for issue in issues_data]
        return issues
    else:
        print(f"Failed to fetch issues for {owner}/{repo} (Status code: {response.status_code})")
        return []


def fetch_issue_commits(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/commits"
    print(f"Issue URL: {url}")  # Debugging url
    response = requests.get(url, headers={'Authorization': f'token {access_token}'})
    if response.status_code == 200:
        commits_data = response.json()
        commit_messages = [commit['commit']['message'] for commit in commits_data]
        return commit_messages
    else:
        print(f"Failed to fetch commit messages for issues #{issue_number} in {owner}/{repo} "
              f"(Status code: {response.status_code})")
        return []


def fetch_issues_code_changes(owner, repo):
    issues_list = fetch_issues(owner, repo)
    commit_messages = []

    for issues in issues_list:
        issues_number = issues[0]
        commit_messages = fetch_issue_commits(owner, repo, issues_number)

    bug_fix_commits = []

    for commit_message in commit_messages:
        if search_bug_fix_terms(commit_message):
            bug_fix_commits.append(commit_message)

    issues_bug_fix_changes = {}
    for commit_message in bug_fix_commits:
        commit_sha = get_commit_sha_by_message(owner, repo, commit_message)
        if commit_sha:
            changes = fetch_commit_diff(owner, repo, commit_sha)
            issues_bug_fix_changes[commit_message] = changes

    return issues_bug_fix_changes


#############################
# End Pull Requests/Issues
#############################


def search_bug_fix_terms(text):
    """
    Search for bug fix terms in the text
    :param text: The text to search
    :return: Boolean
    """
    bug_fix_terms = ["fix", "fixed", "bug", "issue", "resolve", "close"]
    for term in bug_fix_terms:
        if term in text.lower():
            return True
    return False


def check_failed_patches(reps):
    """
    Check if a repository has failed patches
    :param reps: The repository name
    :return: Boolean
    """
    # GitHub API endpoint for searching repositories
    url = f'https://api.github.com/search/repositories?q={reps}'

    response = requests.get(url, headers={'Authorization': f'token {access_token}'})

    if response.status_code == 200:
        data = response.json()
        if data['total_count'] > 0:
            # Get the URL of the first repository found
            repo_url = data['items'][0]['html_url']
            print(f"Repository '{reps}' found at: {repo_url}")
            # Add your code here to clone or download the repository using the repo_url
            # print(data)
            repositories = data["items"]
            # print(repositories)
            quantum_programs = extract_quantum_programs(repositories)
            print(quantum_programs)
            code_diff = process_commit_data(quantum_programs)
            print(code_diff)
        else:
            print(f"Repository '{reps}' not found.")
    else:
        print("Failed to fetch repository information.")


def main():
    """
    Main function to fetch data from GitHub API and save it to a CSV file.
    :return:
    """
    # Main function accepts arguments from command line if given else uses default values
    if len(sys.argv) > 1:
        arg_repo = sys.argv[1]
        # Create a list of dictionaries
        print(arg_repo)
        # extract problematic patches from programs with exactly this repo name
        check_failed_patches(arg_repo)
        exit(0)

    # Adjust the query and language as needed
    # Adding more query words to increase the number of results
    # keywords = ["quantum", "qiskit", "cirq", "QML", "DWAVE"]
    # query = " OR ".join(kw.lower() for kw in keywords)  # Combine keywords with OR operator
    # print(f"Query: {query}")

    # Define the quantum programming languages to include in the search
    # languages = ["python", "javascript", "java", "c++", "c#", "qml", "q#", "quil"]

    # Combine languages with OR operator
    # language = " OR ".join([f"language:{lang}" for lang in languages])
    # print(f"Language: {language}")

    output_repo_file = "MISC/quantum_programs_ext.csv"  # CSV file to save the data
    output_commit_file = "MISC/code_changes_ext.csv"  # CSV file to save the commits

    # Create an instance of the GitHub class
    git_instance = Github(auth=auth)

    # Public Web GitHub
    qp = get_repo_names(git_instance)

    # To close connections after use
    git_instance.close()

    """# query = "dwave OR quantum OR cirq OR qml OR qiskit"
    query = "dwave OR quantum"
    stars = 0  # Number of minimum stars
    # language = "python"  # Specify the programming language if needed

    max_results = 100  # Maximum number of repositories to retrieve

    repositories = search_github_repositories(query, stars, max_results)
    # print(f"Total repositories found: {repositories}")

    quantum_programs = extract_quantum_programs(repositories)"""
    save_to_csv(qp, output_repo_file)
    print(f"List of Repositories saved to: {output_repo_file}")

    code_diff = process_commit_data(qp)
    save_to_csv(code_diff, output_commit_file)
    print(f"List of Commits saved to: {output_commit_file}")

    """# From the quantum_programs, extract the owner and repository name for each program
    for program in quantum_programs:
        owner = program["owner"]
        repo = program["name"]
        bug_fix_changes = fetch_code_changes(owner, repo)

        for commit_message, changes in bug_fix_changes.items():
            print(f"Commit Message: {commit_message}")
            for filename, patch in changes:
                print(f"File: {filename}")
                print("Changes:")
                # print(patch)
                code_diff[filename] = patch
                print("\n")

        pull_bug_fix_changes = fetch_pull_request_code_changes(owner, repo)
        for pull_commit_messages, code_change in pull_bug_fix_changes.items():
            print(f"Pull Commit Message: {pull_commit_messages}")
            for filename, patch in code_change:
                print(f"File: {filename}")
                print("Changes:")
                print(patch)
                code_diff[filename] = patch
                print("\n")

        pull_issues_fix_changes = fetch_issues_code_changes(owner, repo)
        for issue_commit_messages, code_changes in pull_issues_fix_changes.items():
            print(f"Issue Commit Message: {issue_commit_messages}")
            for filename, patch in code_changes:
                print(f"File: {filename}")
                print("Changes:")
                print(patch)
                code_diff[filename] = patch
                print("\n")"""

    print("Done!")


if __name__ == "__main__":
    main()
