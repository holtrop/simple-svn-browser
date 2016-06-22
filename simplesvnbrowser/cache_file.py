import xdg.BaseDirectory
import os

class CacheFile:
    params = None

    def __init__(self):
        if CacheFile.params is None:
            CacheFile.params = {}
            cfp = self.__cache_file_path()
            if os.path.exists(cfp):
                with open(cfp, "r") as f:
                    cache_content = f.read()
                exec(cache_content, CacheFile.params)

    def __cache_dir(self):
        return xdg.BaseDirectory.save_cache_path("simple-svn-browser")

    def __cache_file_path(self):
        return os.path.join(self.__cache_dir(), "settings")
