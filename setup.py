import setuptools


# Specify version
VERSION = '1.0.4'


# Run setup
def readme():
  with open('README.md', 'r') as f:
    return f.read()

setuptools.setup(
  name='roma-console',
  packages=setuptools.find_packages(),
  version=VERSION,
  description='Utilities for print fancy text in terminal.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  author='William Ro',
  author_email='willi4m@zju.edu.cn',
  url='https://github.com/WilliamRo/console',
  download_url='https://github.com/WilliamRo/console/tarball/v' + VERSION,
  license='Apache-2.0',
  keywords=['console', 'terminal', 'color'],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Other Audience",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Artistic Software",
    "Topic :: Printing",
    "Topic :: Utilities",
  ],
)
