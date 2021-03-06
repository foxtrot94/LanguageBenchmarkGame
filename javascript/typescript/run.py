#!/usr/bin/env python

import os

output_dir = os.path.join('.','build')
output_file_name = os.path.join(output_dir, 'program.js')

def setup():
    import subprocess, datetime
    if os.path.exists(os.path.join(os.getcwd(), "setup.log")):
        print("'setup.log' exists. Typescript implementation setup correctly")
        return

    print("Watch for Errors - Requires nodejs, npm and typescript compiler")
    try:
        with open('setup.log', 'w') as logFile:
            logFile.write("# This is an autogenerated file made by 'run.py' on {}\n".format(datetime.datetime.now()))
            logFile.write("# => DO NOT DELETE THIS FILE OR SETUP WILL BE CALLED AGAIN\n")
            logFile.flush()
            subprocess.run(["node", "-v"], stdout = logFile, stderr = logFile, check=True)
            subprocess.run(["npm", "-v"], stdout = logFile, stderr = logFile, check=True)
            subprocess.run(["npm", "install", "typescript", "-g"], stdout = logFile, stderr = logFile, check=True)
            subprocess.run(["npm", "install"], stdout = logFile, stderr = logFile, check=True)

            subprocess.run(["tsc", "-v"], stdout = logFile, stderr = logFile, check=True)
            logFile.flush()
            logFile.write("\n# Setup completed on {}".format(datetime.datetime.now()))
        #end logFile
    except Exception as e:
        print(e)
        if os.path.exists('setup.log'):
            os.remove('setup.log')
#end run

def build():
    import subprocess
    retcode = subprocess.call(['tsc', '-p', './', '--outDir',  output_dir])
    if retcode != 0:
        raise AssertionError("Build failed")
    print("Successfully transpiled Typescript implementation")
#end run

def run(cmd_args):
    import subprocess
    process_args = ["node", output_file_name] + cmd_args
    retcode = subprocess.call(process_args)
    if retcode != 0:
        raise RuntimeError("Program run returned non-zero exit code")
#end run

if __name__=="__main__":
    import sys, os

    setup()
    build()
    if os.path.basename(sys.argv[0]) == os.path.basename(__file__):
        run(sys.argv[1:])
# end main