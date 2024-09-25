from setuptools import setup, find_packages

setup(
    name='finsolvepy',
    version='0.1.0',
    description='A package to solve financial problems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vengatesh K',
    author_email='youremail@example.com',
    url='https://github.com/vengateshk18/finsolvepy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas',          # For data manipulation
        'requests',        # For making HTTP requests
        'python-dotenv',   # For loading environment variables
    ],
    include_package_data=True,
)
