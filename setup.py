from setuptools import setup, find_packages

setup(
    name="ptit-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "requests",
        "pydantic"
    ],
    entry_points={
        'console_scripts': [
            'ptit-server=ptit_server.server:main',
        ],
    },
    author="chiendepvl",
    author_email="vucongchien204@gmail.com",
    description="PTIT Student Assistant Server using FastMCP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ptit-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)