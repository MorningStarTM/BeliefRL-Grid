from setuptools import setup

setup(
    name="tom-pacman-env",
    version="0.1.0",
    packages=["pac_man"],  # Only install this package!
    install_requires=["gymnasium", "pygame", "numpy"],
)
