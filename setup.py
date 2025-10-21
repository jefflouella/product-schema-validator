"""
Schema Validator - Web-based Product Schema Validation Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="schema-validator-web",
    version="2.0.0",
    description="Web-based schema.org Product schema validator with anti-bot bypass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Schema Validator Team",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "flask>=3.0.0",
        "flask-socketio>=5.3.0",
        "python-socketio>=5.10.0",
        "playwright>=1.40.0",
        "jsonschema>=4.20.0",
        "validators>=0.22.0",
        "jinja2>=3.1.2",
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "tqdm>=4.66.1",
        "openpyxl>=3.1.5",
    ],
    entry_points={
        "console_scripts": [
            "schema-validator=schema_validator.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="schema validation seo structured-data product-schema",
    project_urls={
        "Documentation": "https://github.com/yourusername/schema-validator",
        "Source": "https://github.com/yourusername/schema-validator",
        "Bug Reports": "https://github.com/yourusername/schema-validator/issues",
    },
)

