## DevPackage

Command line tools to help you develop your package.


# Preview

```
> devp init mypack -license mit --md 
> cd mypack
> ls -a
./  ../  .meta_version  LICENSE  README.md  build/  docs/  mypack/  setup.py  test/

> cat setup.py

from setuptools import setup, find_packages
...

with Path('README.md').open() as readme:
    readme = readme.read()
...
setup(
    name='mypack',
    ...
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.6.0',
    url='https://github.com/thautwarm/mypack',
    author='thautwarm',
    author_email='twshere@outlook.com',
    ...
    entry_points={"console_scripts": []},
    # above option specifies commands to be installed,
    # e.g: entry_points={"console_scripts": ["devp=devpackage.cli:run"]}
    install_requires=["devpackage"],
    platforms="any",
    ...
)

if isinstance(version, Version):
    meta_version = Path(".meta_version").open("w")
    version.increment(2, 1)
    for i in range(2, 0, -1): version.carry_over(i, 42)
    meta_version.write("method: autoinc\n")
    meta_version.write(f"current: {version}")

> python setup.py install && python -c "import mypack"
hello community, I'm thautwarm

> cat .meta_version
method: autoinc
current: 0.0.2

```

# Install & Requirements

Type `pip install -U devpackage` to install.  

Requires:
- wisepy
- lice

# Usage

- `devp init` , Create a python package template and render some arguments using your git information.


```
devp init <package name>
[-license <license name>]
[-pyversion <describe python version requires>]
[--md: use markdown as README instead of restructuredtext]
[--generation: make a <package name>/generation directory, for codegen]
[--timeversion: use timestamp to version your package when building]
[--autoversion: use auto counting to version your package when building]
```


- `devp clean` , Remove `build/`, `*.egg-info/`, `dist` after building your package.


Here are the descriptions of `devp` command:

```
shell> devp --help 
Available commands:
  clean
      clean some build caches


  init
      initialize developing python package.
      optional:
      --generation
          this project contains generated files.

      --autoversion
          default version decider, even if you don't specify this option.
          automatically increment package's version.
          if `--timeversion` is set, this option will be ignored.

      --timeversion
          automatically generate package's unique version through timestamp.

      --md
          use markdown as README.


  - package_name(positional or keyword arg)          : <class 'str'>
  - license(positional or keyword arg) = 'MIT'
  - pyversion(positional or keyword arg) = '>=3.6.0'
  - kwargs(**kwargs)

```