from setuptools import setup, find_packages, setuptools

setup(
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    name='pv_sizing',
    version='0.7.2',
    license='MIT',
    author="Kiril Ivanov Kurtev",
    author_email='brakisto2015@gmail.com',
    packages=['pv_sizing/dimension', 'pv_sizing/utils'],
    package_dir={'': 'src'},
    url='https://github.com/brakisto/PV-sizing',
    keywords='photovoltaic sizing batteries financial analysis',
    install_requires=[
          'numpy',
          'numpy-financial',
          'pandas',
          'pvlib'
      ],
    include_package_data=True,
    package_data={'pv_sizing/utils': ['example_data/*.csv']},
      )


