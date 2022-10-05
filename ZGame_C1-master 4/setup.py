from setuptools import setup, find_packages

setup(name='gym_zgame',
      version='1.0.2',
      install_requires=['gym>=0.2.3',
                        'pandas',
                        'numpy',
                        'pyfiglet',
                        'uuid',
                        'stable-baselines'],
      packages=find_packages(),
)
