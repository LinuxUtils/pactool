from setuptools import setup, find_packages

setup(
    name="pactool-linuxutils",
    version="1.0.2",
    author="LinuxUtils",
    author_email="thelinuxutils@gmail.com",
    description="A cross-distro package management helper for Linux systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LinuxUtils/pactool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'pactool=pactool:main',
        ],
    },
)