from setuptools import setup, find_packages

setup(
    name='finsolvepy',
    version='1.5.0',
    description='A package to solve financial problems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vengatesh K',
    author_email='vengatesh00014@example.com',
    url='https://github.com/vengateshk18/finsolvepy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',  # Supports Python 3.11
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7,<4.0',  # Specifies Python version requirements
    install_requires=[
        'pandas>=1.0.0,<3.0.0',         # Specify compatible pandas version
        'requests>=2.0.0,<3.0.0',       # Specify compatible requests version
        'python-dotenv>=0.10.2',  # Specify compatible python-dotenv version
    ],
    include_package_data=True,
    package_data={
        'finsolvepy': ['database/*.csv']  # Include CSV files in the package
    },
)
