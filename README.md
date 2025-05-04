# GitHubTYPR

A command-line tool for interacting with GitHub repositories and user accounts.

## Features

- List repositories for a user or yourself
- Create new repositories
- Delete repositories
- Query and filter repositories with JMESPath
- Multiple output formats (table, json, yaml)

## Installation

```bash
pip install githubtypr
```

## Usage

```bash
# List your repositories
githubtypr repo list

# List repositories for a specific user
githubtypr repo list --user username

# Create a new repository
githubtypr repo create --repo repo-name

# Create a private repository
githubtypr repo create --repo repo-name --private

# Delete a repository
githubtypr repo delete --user username --repo repo-name

# Filter repositories with JMESPath query
githubtypr repo list --query "[?language=='Python']"

# Sort repositories by a field
githubtypr repo list --sort-by name
```
