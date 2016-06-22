import simplesvnbrowser
import re

def run(argv):
    url = None
    wc_path = "."
    if len(argv) >= 2:
        if re.search(r'://', argv[1]):
            url = argv[1]
        else:
            wc_path = argv[1]
    if url is None:
        url = determine_url_from_wc(wc_path)
    # TODO: start with url

def determine_url_from_wc(path):
    stdout, _ = simplesvnbrowser.run_svn(["info", path])
    m = re.search(r'^URL: (.*)$', stdout, re.MULTILINE)
    if m is not None:
        return m.group(1)
    return ""
