# Contributing to AYLYS

First off, thank you for considering contributing to ATLYS! It's people like you that make ATLYS such a great tool for blockchain interoperability.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Pull Request Process](#pull-request-process)
5. [Coding Standards](#coding-standards)
6. [Security Issues](#security-issues)
7. [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. 

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip
- virtualenv or conda
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone git@github.com:dewitt4/ATLYS-blockchain-protocol.git
cd ATLYS-blockchain-protocol
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -r requirements/dev.txt
```

5. Set up pre-commit hooks:
```bash
pre-commit install
```

## Development Process

### Branches

- `main`: Latest stable release
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

### Creating a New Feature

1. Create a new branch from `develop`:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

2. Write your code and tests
3. Run tests locally:
```bash
pytest
```

4. Commit your changes:
```bash
git add .
git commit -m "feat: description of your changes"
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR against the `develop` branch
6. Wait for code review
7. Address review comments
8. Await approval and merge

### Commit Message Guidelines

We follow the Conventional Commits specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat(bridge): add support for Solana chain

- Implement Solana transaction verification
- Add state sync for Solana accounts
- Update documentation
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use descriptive variable names
- Document all public APIs

### Example:

```python
from typing import List, Optional

def process_transaction(
    tx_hash: str,
    amount: float,
    recipients: List[str],
    metadata: Optional[dict] = None
) -> bool:
    """Process a cross-chain transaction.

    Args:
        tx_hash: The transaction hash
        amount: The transaction amount
        recipients: List of recipient addresses
        metadata: Optional transaction metadata

    Returns:
        bool: True if transaction was successful
    """
    pass
```

### Documentation

- Use docstrings for all public modules, functions, classes, and methods
- Keep documentation up to date with code changes
- Include examples in docstrings
- Update relevant guides and tutorials

## Security Issues

### Security Considerations

- Never commit sensitive information
- Always review dependencies for vulnerabilities
- Follow secure coding practices
- Use strong cryptographic primitives

## Community

### Getting Help

- GitHub Issues: Bug reports and feature requests
- Discord: Community discussions and support
- Telegram: Quick questions and updates
- Forum: Long-form discussions and proposals

### Making Non-Code Contributions

- Write documentation
- Create tutorials
- Answer questions
- Report bugs
- Suggest features
- Review pull requests