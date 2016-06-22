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
      )
