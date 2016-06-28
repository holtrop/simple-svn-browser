import sys
if sys.version_info < (3, 5):
    print("Python 3.5 is required for this package")
    sys.exit(1)

from setuptools import setup

setup(name = "simplesvnbrowser",
      version = "0.0.1",
      description = "A simple subversion repository browser application",
      url = "https://github.com/holtrop/simple-svn-browser",
      author = "Josh Holtrop",
      author_email = "jholtrop@gmail.com",
      license = "zlib",
      packages = ["simplesvnbrowser"],
      zip_safe = False,
      scripts = ["bin/simple-svn-browser"],
      install_requires = ["pygobject", "pyxdg"],
      )
