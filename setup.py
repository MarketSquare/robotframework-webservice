from setuptools import find_packages, setup
from RobotFrameworkService.version import get_version

CLASSIFIERS = """
Development Status :: 3 - Alpha
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Framework :: Robot Framework
Framework :: Robot Framework :: Tool
Programming Language :: Python :: 3.9
Programming Language :: Python :: Implementation :: PyPy
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
      author='Deutsche Post Adress GmbH & Co. KG',
      packages=find_packages(),
      install_requires=[
            get_requirements()
      ],
      long_description=get_long_description(),
      url='https://github.com/postadress/robotframework-webservice',
      zip_safe=False)
