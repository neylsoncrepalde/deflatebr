from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='deflateBR',
      version='0.1',
      description='Deflate Nominal Brazilian Reais',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/neylsoncrepalde/deflatebr',
      author='Neylson Crepalde & Fernando Meireles',
      author_email='neylsoncrepalde@gmail.com',
       classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Mathematics'
      ],
      keywords='deflate deflation economics salary wage finance',
      license='MIT',
      packages=['deflatebr'],
      zip_safe=False,
      install_requires=[
          'requests',
          'pandas',
          'numpy',
          'datetime'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      python_requires='>=3.7')