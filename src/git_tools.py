import os

import git

GIT_URL: str = "https://github.com/KorayL/News-Compiler.git"
""" URL of the GitHub repository. """

def pull():
    """
    Checks if the current version is up to date with the latest release on GitHub.
    If not, pull the latest push. After pulling, the latest release is checked out.
    """

    # Get the git repository from parent directory
    repo = git.Repo(os.path.dirname(os.path.dirname(__file__)))

    # Check if the version file exists
    if not os.path.exists("version.txt"):
        with open("version.txt", "w") as file:
            version: str = repo.tags[-1].name
            file.write(version)

    # Get current version number
    with open("version.txt", "r") as file:
        version = file.read().strip()

    # Get the latest release version number
    repo.remotes.origin.fetch()
    latest_version_name = repo.tags[-1].name

    # Pull the latest release if not up to date
    if version != latest_version_name:
        print("Pulling Latest Release from GitHub...")
        # git pull origin main
        repo.remotes.origin.pull("main")
        with open("version.txt", "w") as file:
            file.write(latest_version_name)

        # Checkout latest release
        repo.git.checkout(repo.tags[-1].commit.hexsha)
        print("Checked out Latest Release")

def initialize():
    """
    Initializes the git repository, sets origin to the GitHub repository and resets the repository to the latest release.
    :return:
    """

    # Get the parent directory of the current file
    repo_path = os.path.dirname(os.path.dirname(__file__))

    # Initialize git repository to parent directory
    git.Repo.init(repo_path)  # Initialize git repository
    repo = git.Repo(repo_path)  # Get the repository as an object

    # Replace current project with a pull from GitHub
    origin = repo.create_remote("origin", GIT_URL)  # Set origin to remote GitHub repository
    origin.fetch()  # Fetch the latest release
    repo.git.reset("--hard", "origin/main")  # Hard reset

    # Checkout latest release
    repo.git.checkout(repo.tags[-1].commit.hexsha)

    # Write the latest release to version file
    with open("version.txt", "w") as file:
        file.write(repo.tags[-1].name)

    print("Initialized Repository...")


if __name__ == "__main__":
    pull()
