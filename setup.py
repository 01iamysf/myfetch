from setuptools import setup, find_packages

setup(
    name="myfetch",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["myfetch"],
    entry_points={
        "console_scripts": [
            "myfetch=myfetch:main",
        ],
    },
    author="Antigravity Team",
    description="Advanced Linux System Diagnostics Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
