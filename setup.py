import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='simbak',
    version='0.0.1',
    author='Mark Bromell',
    author_email='markbromell.business@gmail.com',
    description='A simple backup solution that\'s light and portable',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mark-bromell/simbak',
    package=setuptools.find_packages(),
    classifiers=[
        'Programming Languages :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)