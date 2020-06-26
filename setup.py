import setuptools

from jugaad_data import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jugaad Data", # Replace with your own username
    version=__version__,
    description="Jugad data is a library to download historical price-volume data from NSE in pandas dataframe.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://marketsetup.in/documentation/jugaad-data/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)