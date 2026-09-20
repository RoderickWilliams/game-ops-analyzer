from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="game-ops-analyzer",
    version="1.0.0",
    author="RoderickWilliams",
    author_email="roderickwilliams@users.noreply.github.com",
    description="A configurable Game Operations Analysis Agent that generates SaaS-style interactive HTML reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RoderickWilliams/game-ops-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
        "pyyaml>=6.0",
    ],
)
