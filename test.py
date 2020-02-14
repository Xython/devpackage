from devpackage.cli import init, clean
from devpackage.path import Path
from os import chdir, mkdir
from subprocess import check_output
from shutil import rmtree
import sys

mkdir('./test_sample')
chdir('./test_sample')

init("mock_pack1", license="MIT")
init("mock_pack2_qwertyuiopasdfghjkl", license="bsd3", md=True)
chdir('./mock_pack2_qwertyuiopasdfghjkl')

argv = sys.argv
argv.clear()
argv.extend([str(Path("setup.py")), 'install'])

with open('setup.py', 'r', encoding='utf8') as f:
    exec(f.read())
clean()

check_output(['pip', 'uninstall', '-y', 'mock_pack2_qwertyuiopasdfghjkl'])
chdir('../../')
w = Path('./test_sample')
print(type(w))
w.delete()
