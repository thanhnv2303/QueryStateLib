import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QueryStateLib",
    version="1.1.4",
    author="LinLin",
    author_email="nguyenthanh2303@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/thanhnv2303/QueryStateLib",
    project_urls={
        "Bug Tracker": "https://github.com/thanhnv2303/QueryStateLib",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'web3>=5.23.0',
        'requests<=2.26.0',
        'pbkdf2==1.3',
    ]
)