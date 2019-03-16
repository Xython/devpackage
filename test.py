from devpackage.cli import init, clean
from devpackage.disttools.path import Path
from os import chdir, mkdir
from subprocess import check_output
from shutil import rmtree

mkdir('./test_sample')
chdir('./test_sample')

init("mock_pack1", license="MIT")
init("mock_pack2_qwertyuiopasdfghjkl", license="bsd3", md=True)

chdir('./mock_pack2_qwertyuiopasdfghjkl')
check_output(['python', 'setup.py', 'install'])
clean()
check_output(['pip', 'uninstall', '-y', 'mock_pack2_qwertyuiopasdfghjkl'])

chdir('../../')
rmtree('./test_sample')
