from wisepy.talking import Talking
from devpackage.disttools.path import Path
from devpackage.disttools.version import Version
from subprocess import check_output, CalledProcessError
from warnings import warn
talk = Talking()

@talk
def clean():
    """
    clean some build caches
    """
    def check(p: str):
        for each in ('build', '.egg-info', 'dist', '__pycache__'):
            if p.lower().endswith(each):
                return True
        return False

    for each in Path('.').list_dir(check):
        each.delete()

@talk
def init(package_name: str, license='MIT', pyversion=">=3.6.0", **kwargs):
    """
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

    """
    package_name = package_name.strip()
    license = license.strip().lower()
    pyversion = pyversion.strip()


    has_generated_file = ('generated') if 'generation' in kwargs else ()
    try:
        author = check_output(['git', 'config',  'user.name']).decode().strip()
    except CalledProcessError:
        author = None
        warn('git user.author not set, you should configure author manually.')

    # fuck it, I'm a repeater?
    try:
        email = check_output(['git', 'config', 'user.email']).decode().strip()
    except CalledProcessError:
        email = None
        warn('git user.email not set, you should configure email manually.')

    if author:
        repo = f'https://github.com/{author}/{package_name}'
    else:
        repo = ""

    this: Path = Path(package_name)
    if package_name.lower() in (*has_generated_file, 'docs', 'test', 'build', 'setup.py', 'requirements.txt', '.meta_version', 'README.rst', 'README.md', 'LICENSE'):
        raise NameError(f"{package_name} is not a valid package name")

    if not this.exists():
        this.mkdir()

    license_filepath = this.into('LICENSE').abs()
    check_output(['lice', license, '-f', license_filepath])
    # python source code package
    this.into(package_name).mkdir()

    this.into('docs').mkdir()
    this.into('test').mkdir()
    this.into('build').mkdir()
    init_version = Version("0.0.1")

    if has_generated_file:
        this.into('generated').mkdir()


    with this.into('setup.py').open(mode='w') as f:
        with this.into('.meta_version').open(mode='w') as meta_version:
            if 'timeversion' in kwargs:
                meta_version.write('method: timeversion')
            else:
                meta_version.write('method: autoinc\n')
                meta_version.write(f'current: {init_version}')

        def w(buf, indent=0):
            indent = '    ' * indent
            f.write(indent + buf + '\n')

        w('from setuptools import setup, find_packages')
        w('from datetime import datetime')
        w('from devpackage.disttools.version import Version')
        w('from devpackage.disttools.path import Path')
        w('\n')
        w('with open(".meta_version", "r") as meta_version:')
        w('meta_version_config = dict(each.strip().split(":") for each in meta_version.read().splitlines())', indent=1)
        w('version_method = meta_version_config.get("method")')
        w('\n')
        w('if version_method is None:')
        w(f'version = {str(init_version)!r}', indent=1)
        w('elif version_method.strip() == "timeversion":')
        w('version = datetime.today().timestamp()', indent=1)
        w('elif version_method.strip() == "autoinc":')
        w('version = Version(meta_version_config["current"].strip())', indent=1)
        w('else: raise Exception("Invalid `version_method`. Check your .meta_version.")')
        w('\n')
        use_md = 'md' in kwargs
        readme_filename = 'README.' + ('md' if use_md else 'rst')
        w(f'with Path({readme_filename!r}).open() as readme:')
        w('readme = readme.read()', indent=1)
        w('\n')
        w('setup(')

        def ww(a):
            return w(a, indent=1)

        ww(f'name={package_name!r},')
        ww(f'version=version if isinstance(version, str) else str(version),')

        ww('keywords="", # keywords of your project that separated by comma ","')
        ww('description="", # a conceise introduction of your project')
        ww('long_description=readme,')

        if use_md:
            with this.into('README.md').open('w') as readme:
                readme.write(f'## {package_name}')
            ww('long_description_content_type="text/markdown",')
        else:
            with this.into('README.rst').open('w') as readme:
                readme.write(f'{package_name}\n')
                readme.write('====' * len(package_name))

        ww(f'license={license!r},')
        ww(f'python_requires={pyversion!r},')
        ww(f'url={repo!r},')
        ww(f'author={author!r},')
        ww(f'author_email={email!r},')
        ww(f'packages=find_packages(),')
        ww('entry_points={"console_scripts": []},')
        ww('# above option specifies commands to be installed,')
        ww('# e.g: entry_points={"console_scripts": ["yapypy=yapypy.cmd.compiler"]}')
        ww('install_requires=["devpackage"],')
        ww('platforms="any",')
        ww('classifiers=[')
        w('"Programming Language :: Python :: 3.6",', indent=2)
        w('"Programming Language :: Python :: 3.7",', indent=2)
        w('"Programming Language :: Python :: Implementation :: CPython",', indent=2)
        ww('],')
        ww('zip_safe=False,')
        w(')')
        w('\n')
        w('if isinstance(version, Version):')
        ww('meta_version = Path(".meta_version").open("w")')
        ww('version.increment(2, 1)')
        ww('for i in range(2, 0, -1): version.carry_over(i, 42)')
        ww(r'meta_version.write("method: autoinc\n")')
        ww('meta_version.write(f"current: {version}")')

        with this.into(package_name).into('__init__.py').open('w') as init_file:
            init_file.write(f'print ("hello community, I\'m {author}!")')

def run():
    talk.on()
