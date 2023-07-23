from distutils.core import setup
import vncrevolver

setup(name="vncrevolver",
      version=vncrevolver.__version__,
      author="cristiancmoises",
      url="https://github.com/cristiancmoises/vncrevolver",
      install_requires=["pydantic", "asyncvnc", "aiohttp"])
