from setuptools import setup, find_packages
import os

# setup.pyがあるディレクトリをベースとする
current_dir = os.path.abspath(os.path.dirname(__file__))
# パッケージのソースディレクトリ (webdetakit/webdetakit/)
package_source_dir = os.path.join(current_dir, 'webdetakit')

setup(
    name="webdetakit",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful toolkit for web scraping and data normalization.",
    long_description=open(os.path.join(current_dir, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kongou173/webdetakit", 
    packages=find_packages(where=current_dir, include=['webdetakit', 'webdetakit.*']), 
    package_dir={'webdetakit': package_source_dir}, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.6.3",
        "pandas>=1.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.2",
            "twine>=3.4.1",
            "setuptools>=59.6.0",
            "wheel>=0.37.0",
        ]
    }
)
