#!/usr/bin/env python

output_name = './build/libs/java.jar'

def setup():
    import os, datetime, subprocess
    if os.path.exists(os.path.join(os.getcwd(), "setup.log")):
        print("'setup.log' exists. Java implementation setup correctly")
        return

    print("Watch for Errors - Requires Java SDK and Runtime")

    try:
        with open('setup.log', 'w') as logFile:
            logFile.write("# This is an autogenerated file made by 'run.py' on {}\n".format(datetime.datetime.now()))
            logFile.write("# => DO NOT DELETE THIS FILE OR SETUP WILL BE CALLED AGAIN\n")
            logFile.flush()
            subprocess.run(["javac", "-version"], stdout = logFile, stderr = logFile, check=True)
            subprocess.run(["gradle", "-v"], stdout = logFile, stderr = logFile, check=True)
            subprocess.run(["java", "--version"], stdout = logFile, stderr = logFile, check=True)
            logFile.flush()
            logFile.write("\n# Setup completed on {}".format(datetime.datetime.now()))
        #end logFile
    except Exception as e:
        print(e)
        if os.path.exists('setup.log'):
            os.remove('setup.log')
#end run

def build():
    import os, subprocess
    retcode = subprocess.call(["gradle", "fullBuild"])
    if retcode != 0:
        raise AssertionError("Build failed")

    print("Built Java implementation as {}".format(output_name))
#end run

def run(cmd_args):
    import subprocess
    retcode = subprocess.call(["java", "-jar", output_name] + cmd_args)
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
        
