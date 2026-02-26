# Contributing to POMODORO TIMER

Thank you for considering contributing to POMODORO TIMER! This document outlines the process for contributing, provides guidance on setting up your development environment, and contains other essential information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Code Contributions](#code-contributions)
3. [Development Setup](#development-setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Database Setup](#database-setup)
   - [Running the Project](#running-the-project)
4. [Style Guide](#style-guide)
5. [Changelog](#changelog)
6. [License](#license)

## Code of Conduct

We pledge to act and interact in ways that contribute to an open, welcoming, diverse, inclusive, and healthy community. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) for detailed guidelines.

## How Can I Contribute?

### Reporting Bugs

If you encounter a bug, please report it using our issue tracker on GitHub. Make sure to include:

- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected behavior.
- Actual behavior.
- Additional information (e.g., error messages, screenshots, etc.).

### Suggesting Features

We welcome suggestions for new features! To suggest a feature:

- Search our issue tracker to see if it has already been proposed.
- Create a new issue with a comprehensive description of the feature, including its purpose and possible implementation strategies.

### Code Contributions

If you are interested in contributing code, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes, committing as necessary.
4. Push your changes to your fork.
5. Open a pull request on the main repository, ensuring to describe the changes and related issues.

## Development Setup

### Prerequisites

You will need:

- [Python](https://www.python.org/) (version 3.x recommended)
- [pip](https://pip.pypa.io/en/stable/) for managing Python packages

### Installation

Clone the repository and install the required dependencies by running:

```bash
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
uv sync
```

### Database Setup

This project uses a SQLite database to manage tasks. The database schema will be automatically created when you first run the application. No additional setup is required beyond installation.

### Running the Project

To start the application, use the following command:

```bash
python pomodoro.py -i
```

This command launches the interactive command-line interface.

## Style Guide

We adopt standard Python conventions and encourage contributors to adhere to them for consistency and readability. Please follow PEP 8 guidelines and use descriptive variable names.

## Changelog

We maintain a [CHANGELOG.md](CHANGELOG.md) file in the repository, detailing updates, bug fixes, and new features with every release. Keeping this file up to date will help users understand the project’s progress.

## License

This project is licensed under the [MIT License](LICENSE). By contributing, you agree that your contributions will be licensed under the same terms.

We appreciate your efforts and look forward to your contributions to make POMODORO TIMER even better!
