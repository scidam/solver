from setuptools import setup

def parse_requirements(filename):
    return list(filter(lambda line: (line.strip())[0] != '#',
                       [line.strip() for line in open(filename).readlines()]))

README_FILE = 'README.rst'

setup(name='pysolver',
      packages=['solver'],
      version='0.0.3',
      description='Make problem solving process easier',
      keywords='Python solver, problem solver,\
task templates,solution templates engine, computational problems, mathematics',
      long_description=open(README_FILE).read(),
      include_package_data=True,
      install_requires=parse_requirements('requirements.txt'),
      author='Dmitry E. Kislov',
      author_email='kislov@easydan.com',
      url='https://github.com/scidam/solver',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Education',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Mathematics',
          ],
      )
