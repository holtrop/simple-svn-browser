import subprocess

def run_svn(args):
    completed_process = subprocess.run(
            ["svn", "--non-interactive"] + args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    return completed_process.stdout.decode(), completed_process.stderr.decode()
