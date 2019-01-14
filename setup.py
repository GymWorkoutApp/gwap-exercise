import setuptools
from setuptools import find_packages
import src


def long_description():
    with open('README.md', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='gwa_common',
    version=src.__version__,

    url='',
    description='Microservice that keep endpoints commons to GWA.',
    long_description=long_description(),
    long_description_content_type="text/markdown",

    author='Guilherme Dalmarco',
    author_email='dalmarco.br@gmail.com',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    include_package_data=True,
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    extras_require={},
)
