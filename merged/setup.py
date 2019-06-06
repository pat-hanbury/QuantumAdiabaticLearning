# several files with ext .pyx, that i will call by their name
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("lib.qvmc.utils", ["lib/qvmc/utils.pyx"]),
    Extension("lib.qvmc.state", ["lib/qvmc/state.pyx"]),
    Extension("lib.qvmc.optimizer", ["lib/qvmc/optimizer.pyx"]),
    Extension("lib.qvmc.debug", ["lib/qvmc/debug.pyx"]),
    Extension("lib.qvmc.hamiltonian", ["lib/qvmc/hamiltonian.pyx"]),
]

setup(
  name = 'VMCS',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)