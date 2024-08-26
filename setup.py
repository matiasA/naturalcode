from setuptools import setup, find_packages

setup(
    name="naturalcode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy==3.5.3",
        "numpy==1.24.3",
        "scikit-learn==1.2.2",
    ],
    extras_require={
        "dev": [
            "pytest==7.3.1",
            "black==23.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "naturalcode=naturalcode.cli:main",
        ],
    },
    author="NaturalCode Team",
    author_email="info@naturalcode.com",
    description="Un lenguaje de programación basado en lenguaje natural para aplicaciones web CRUD",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/naturalcode/naturalcode",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)