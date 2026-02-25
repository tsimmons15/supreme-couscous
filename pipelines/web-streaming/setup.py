from setuptools import find_packages, setup

setup(
    name='aeo-web-streaming',
    version='1.0.0',
    description='AEO Web Events Streaming Pipeline',
    packages=find_packages(),
    install_requires=['apache-beam[gcp]==2.59.0'],
    entry_points={
        'console_scripts': ['aeo-web-stream=streaming_pipeline:run_pipeline'],
    },
)
