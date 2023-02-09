from distutils.core import setup
setup(
  name = 'PandasDB',
  packages = ['PandasDB'],
  version = '1.0',      
  license='MIT',
  description = 'PandasDB is a lightweight library that combines the power of SQLite databases with the ease of use of Python numerical libraries like pandas, numpy, scipy, etc.',
  author = 'Marcel Ferrari',
  author_email = 'mferrari@ethz.ch',      # Type in your E-Mail
  url = 'https://github.com/MarcelFerrari/PandasDB',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MarcelFerrari/PandasDB/archive/refs/tags/v1.0.tar.gz',    # I explain this later on
  keywords = ['Pandas', 'SQL', 'Database', 'Numerical Python', 'SQLite', 'Data science', 'Jupyter notebook'],   # Keywords that define your package best
  install_requires=['pandas'],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    # 'Programming Language :: Python :: 3.4',
    # 'Programming Language :: Python :: 3.5',
    # 'Programming Language :: Python :: 3.6',
  ],
)