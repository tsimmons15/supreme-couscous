from setuptools import find_packages, setup

setup(
    name='aeo-pos-batch',
    version='1.0.0',
    description='AEO POS Batch Pipeline',
    packages=find_packages(),
    install_requires=['apache-beam[gcp]==2.59.0'],
    entry_points={
        'console_scripts': ['aeo-pos-batch=pipeline:run_pipeline'],
    },
)
