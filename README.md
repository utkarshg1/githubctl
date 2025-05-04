# GitHubCTL

A command-line tool for interacting with GitHub repositories and user accounts.

## Features

- List repositories for a user or yourself
- Create new repositories
- Delete repositories
- Query and filter repositories with JMESPath
- Multiple output formats (table, json, yaml)

## Installation

```bash
pip install githubctl
```

## Usage

```bash
# List your repositories
githubctl repo list

# List repositories for a specific user
githubctl repo list --user username

# Create a new repository
githubctl repo create --repo repo-name

# Create a private repository
githubctl repo create --repo repo-name --private

# Delete a repository
githubctl repo delete --user username --repo repo-name

# Filter repositories with JMESPath query
githubctl repo list --query "[?language=='Python']"

# Sort repositories by a field
githubctl repo list --sort-by name
```

## Development

To contribute to this project, clone the repository and install dependencies:

```bash
git clone https://github.com/utkarshg1/githubctl.git
cd githubctl
pip install -e .
```
