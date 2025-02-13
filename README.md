# Coastal Land Use & Marine Plastic Analysis

A Flask web application for analyzing land use patterns and marine plastic concentration in coastal areas. The app provides interactive visualizations and detailed environmental metrics for both developed and developing coastal cities.

## Prerequisites

Before you begin, ensure you have the following installed on your Mac:

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Homebrew (recommended for managing packages)

## Installation

1. Install Python and pip (if not already installed):
```bash
brew install python
```

2. Clone the repository:
```bash
git clone https://github.com/mgkram4/data-world-platic.git
cd data-world-platic
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

4. Install required packages:
```bash
pip install flask numpy requests
```

## Running the Application

1. Make sure you're in the project directory with your virtual environment activated

2. Start the Flask development server:
```bash
python main.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
├── static/
│   └── style.css       # CSS styles for the application
├── templates/
│   ├── error.html      # Error page template
│   ├── index.html      # Home page template
│   ├── query.html      # Query form template
│   └── results.html    # Results display template
├── main.py             # Main Flask application file
└── README.md           # Project documentation
```

## Making Contributions

### Setting Up for Development

1. Fork the repository through GitHub

2. Clone your fork:
```bash
git clone https://github.com/your-username/data-world-platic.git
```

3. Add the original repository as upstream:
```bash
git remote add upstream https://github.com/mgkram4/data-world-platic.git
```

### Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them locally

3. Commit your changes:
```bash
git add .
git commit -m "Description of your changes"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request through GitHub

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add comments for complex functionality
- Update documentation when adding new features
- Write descriptive commit messages
- Test your changes thoroughly before submitting a PR

### Keeping Your Fork Updated

Regularly sync your fork with the main repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

## Features

- Interactive map visualization
- Land use analysis and distribution
- Marine plastic concentration analysis
- Environmental impact assessment
- Comparative analysis of developed and developing coastal regions
- Historical data trends and projections

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue with a detailed description
3. Label the issue appropriately

## License

[Add your license information here]
