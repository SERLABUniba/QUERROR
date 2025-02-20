from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the GitHub credentials
github_username = os.getenv("GITHUB_USERNAME")
github_token = os.getenv("GITHUB_TOKEN")

# Print the credentials
print(f"GitHub Username: {github_username}")
print(f"GitHub Token: {github_token}")
