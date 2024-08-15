import requests
import os

def get_github_repos_and_stars(username):
    # GitHub API URL for user repos
    url = f"https://api.github.com/users/{username}/repos"
    
    # Send request to the GitHub API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for user {username}. HTTP Status code: {response.status_code}")
    
    repos = response.json()
    repo_count = len(repos)
    total_stars = sum(repo['stargazers_count'] for repo in repos)
    
    return repo_count, total_stars

def save_data_to_file(filename, repo_count, total_stars):
    with open(filename, 'w') as file:
        file.write(f"{repo_count}\n")
        file.write(f"{total_stars}\n")

def read_data_from_file(filename):
    if not os.path.exists(filename):
        return None, None

    with open(filename, 'r') as file:
        repo_count = int(file.readline().strip())
        total_stars = int(file.readline().strip())
    
    return repo_count, total_stars

if __name__ == "__main__":
    username = input("Enter your GitHub username: ")
    filename = f"{username}_github_data.txt"

    try:
        # Get the current repo count and stars
        current_repo_count, current_total_stars = get_github_repos_and_stars(username)

        # Read the previous data from file
        previous_repo_count, previous_total_stars = read_data_from_file(filename)

        # Save the current data to file
        save_data_to_file(filename, current_repo_count, current_total_stars)

        # Print the results
        print(f"User '{username}' has {current_repo_count} repositories with a total of {current_total_stars} stars.")

        # Compare with previous values if they exist
        if previous_repo_count is not None and previous_total_stars is not None:
            if current_repo_count < previous_repo_count:
                print(f"Warning: The number of repositories has decreased (was {previous_repo_count}, now {current_repo_count}).")
            if current_total_stars < previous_total_stars:
                print(f"Warning: The total number of stars has decreased (was {previous_total_stars}, now {current_total_stars}).")
        else:
            print("This is the first time data is being recorded.")

    except Exception as e:
        print(e)
