from setuptools import setup, find_packages

setup(
    name="hrfinder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "motor>=3.3.1",
        "pydantic>=2.5.2",
        "pydantic-settings>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
        ]
    },
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="HR Finder API for searching and analyzing LinkedIn profiles",
    keywords="hr, linkedin, profiles, search",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
) 