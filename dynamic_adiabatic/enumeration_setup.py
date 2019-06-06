# several files with ext .pyx, that i will call by their name
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("lib.enumeration_qvmc.utils", ["lib/enumeration_qvmc/utils.pyx"]),
    Extension("lib.enumeration_qvmc.state", ["lib/enumeration_qvmc/state.pyx"]),
    Extension("lib.enumeration_qvmc.optimizer", ["lib/enumeration_qvmc/optimizer.pyx"]),
    Extension("lib.enumeration_qvmc.debug", ["lib/enumeration_qvmc/debug.pyx"]),
    Extension("lib.enumeration_qvmc.hamiltonian", ["lib/enumeration_qvmc/hamiltonian.pyx"]),
]

setup(
  name = 'VMCS',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)