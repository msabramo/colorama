from os.path import dirname, join
from setuptools import setup, find_packages

name = 'colorama'
version = '0.1.1'

def get_long_description(filename):
    readme = join(dirname(__file__), filename)
    return open(readme).read()


setup(
    name=name,
    version=version,
    description="Cross-platform colored terminal text.",
    long_description=get_long_description('README.txt'),
    keywords='color colour terminal text ansi windows crossplatform xplatform',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    url='http://code.google.com/p/colorama/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
# -*- Entry points: -*-
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Terminals',
    ]
    # see classifiers http://pypi.python.org/pypi?%3Aaction=list_classifiers
)

