from setuptools import setup, find_packages

setup(
    name="myfetch-tool",
    version="1.0.1",
    packages=find_packages(),
    py_modules=["myfetch"],
    entry_points={
        "console_scripts": [
            "myfetch=myfetch:main",
        ],
    },
    author="Antigravity Team",
    description="Advanced Linux System Information & Diagnostics Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
