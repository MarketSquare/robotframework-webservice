from setuptools import find_packages, setup
from RobotFrameworkService.version import get_version

CLASSIFIERS = """
Development Status :: 4 - Beta
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Framework :: FastAPI
Framework :: Robot Framework
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
""".strip().splitlines()

def get_long_description():
      with open('README.md','r') as file:
            return file.read()


def get_requirements():
      with open('requirements.txt','r') as file:
            return file.readlines()


setup(name='robotframework-webservice',
      version=get_version(),
      classifiers=CLASSIFIERS,
      description='Webservice for running Robot Framework tasks',
      author='Markus Stahl',
      packages=find_packages(),
      install_requires=[
            get_requirements()
      ],
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      url='https://github.com/MarketSquare/robotframework-webservice',
      zip_safe=False)
