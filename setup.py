from setuptools import find_packages, setup

setup(
    name="chatbot_client",  # Name of the module
    version="0.1.0",  # Version number
    packages=find_packages(),  # Automatically find all packages
    install_requires=[  # List any dependencies that need to be installed
        "requests>=2.26.0",
        "pydantic>=1.8.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Minimum Python version required
)
