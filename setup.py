import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='simbak',
    version='0.4.2',
    author='Mark Bromell',
    author_email='markbromell.business@gmail.com',
    description='A simple backup solution that\'s light and portable',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    url='https://github.com/mark-bromell/simbak',
    project_urls={
        'Source Code': 'https://github.com/mark-bromell/simbak',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'simbak = simbak.__main__:main',
        ],
    },
    install_requires=[
        'python-dotenv'
    ]
)
