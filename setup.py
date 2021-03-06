from setuptools import setup, find_packages


with open('./README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='devpackage',
    version='0.3',
    keywords='developing tools, package development',
    description='',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='mit',
    python_requires='>=3.6.0',
    url='https://github.com/Xython/devpackage',
    author='Xython',
    author_email='twshere@outlook.com',  # billing email
    packages=find_packages(),
    entry_points={'console_scripts': ['devp=devpackage.cli:run']},
    install_requires=['argser', 'lice'],
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    zip_safe=False
)
