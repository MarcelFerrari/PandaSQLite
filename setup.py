from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'PandaSQLite',
  packages = ['PandaSQLite'],
  version = '1.1',      
  license='MIT',
  description = 'PandaSQLite is a lightweight library that combines the power of SQLite databases with the ease of use of Python numerical libraries like pandas, numpy, scipy, etc.',
  author = 'Marcel Ferrari',
  author_email = 'marcel.mfnc@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/MarcelFerrari/PandaSQLite',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MarcelFerrari/PandaSQLite/archive/refs/tags/v1.1.tar.gz',    # I explain this later on
  keywords = ['Pandas', 'SQL', 'Database', 'Numerical Python', 'SQLite', 'Data science', 'Jupyter notebook'],   # Keywords that define your package best
  install_requires=['pandas'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',      
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
  ],
  long_description=long_description,
  long_description_content_type='text/markdown',
)