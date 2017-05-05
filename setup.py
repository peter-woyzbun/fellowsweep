from setuptools import setup


setup(name='fellowsweep',
      version='0.1',
      description='Minesweeper Django challenge.',
      url='http://github.com/peter-woyzbun/',
      author='Peter Woyzbun',
      author_email='peter.woyzbun@gmail.com',
      packages=['fellowsweep'],
      install_requires=['django', 'numpy', 'scipy', 'pandas'],
      zip_safe=False)