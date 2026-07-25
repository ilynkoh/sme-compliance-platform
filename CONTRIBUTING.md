# Contributing to SME Compliance Platform

We welcome contributions! This document explains how to contribute.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Report issues responsibly
- Follow project guidelines

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Provide:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Suggesting Features

1. Describe the feature clearly
2. Explain the use case
3. Provide examples if possible
4. Discuss implementation approach

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following code style
4. Add tests for new functionality
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/sme-compliance-platform.git
cd sme-compliance-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Max line length: 100
- Use black for formatting

### TypeScript/React (Frontend)
- Use consistent indentation
- Follow React best practices
- Use meaningful variable names
- Add comments for complex logic

## Testing Requirements

- Write tests for new features
- Maintain test coverage > 80%
- Run tests before submitting PR

```bash
# Run tests
cd backend
pytest tests/

cd ../frontend
npm test
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code reorganization
- `test`: Tests
- `chore`: Build/dependencies

Example:
```
feat(reports): Add PDF export functionality

Implement PDF export for compliance reports using reportlab.
Allows users to download reports in PDF format.

Closes #123
```

## Pull Request Process

1. Update documentation
2. Add tests for changes
3. Ensure all tests pass
4. Update CHANGELOG
5. Submit PR with clear description
6. Address review feedback
7. Rebase before merge

## Areas for Contribution

### High Priority
- AI analysis improvements
- More compliance checks
- Performance optimization
- Documentation

### Medium Priority
- UI/UX improvements
- Additional file format support
- Email notifications
- Report generation formats

### Low Priority
- Code refactoring
- Additional language support
- Theme customization

## License

By contributing, you agree your code is licensed under MIT License.

## Questions?

Reach out to the team via:
- GitHub Issues
- Email: support@smecompliance.my
- GitHub Discussions
