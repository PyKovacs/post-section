from setuptools import setup

with open("README.MD", "r") as f:
    long_description = f.read()

setup(
    name="post_section",
    version="0.0.10",
    description="Post section provides API interface to post, fetch, update and delete posts.",
    packages=['post_section', 'post_section.source'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyKovacs/post_section",
    author="PyKovacs",
    author_email="PyKovacs",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["SQLAlchemy==1.4.36",
                      "Flask==2.2.3",
                      "Flask-SQLAlchemy==2.5.1",
                      "requests==2.27.1"],
    python_requires=">=3.10",
)