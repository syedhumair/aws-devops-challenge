try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='S3-Inspect',
    version='0.1',
    description='A package to inspect contents of S3 buckets and generate report',
    author='Syed Humair',
    author_email="syed.humair@gmail.com",
    keywords=['aws', 's3', 'challenge'],
    packages=['s3inspect', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    url='https://github.com/syedhumair/aws-devops-challenge',
    install_requires=requirements,
)
