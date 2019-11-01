import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Preflight-Oxyde2", # Replace with your own username
    version="0.5.0",
    author="Oxyde2",
    author_email="iorbital.projects@gmail.com",
    description="Python package for rocket flight simulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oxyde2/Preflight",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
