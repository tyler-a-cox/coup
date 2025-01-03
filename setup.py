from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='coup',
    version='0.1.0',
    keywords='coup',
    packages=find_packages(include=['coup', 'coup.*']),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    author='Tyler Cox',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tyler-a-cox/coup',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)