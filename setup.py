from setuptools import setup

setup(
    name="gaia",
    version="0.1.0",
    py_modules=["gaia"],
    install_requires=["click"],
    author="Guilherme Alves Pimenta",
    author_email="guilherme@goentri.com",
    description="Gaia is a cli tool to help you create new lambda functions following a pre-defined structure.",
    entry_points={"console_scripts": ["gaia=gaia:gaia"]},
)
