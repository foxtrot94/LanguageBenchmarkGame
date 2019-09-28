#!/usr/bin/env python

output_file_name = 'golang.out'

def setup():
    import os, subprocess, datetime
    if os.path.exists(os.path.join(os.getcwd(), "setup.log")):
        print("'setup.log' exists. Go implementation setup correctly")
        return

    # We can't really setup this successfully, we need a build system like CMake or scons for xplat support
    print("Watch for Errors - Requires Go")
    dependencies = ["github.com/deckarep/golang-set", "github.com/karrick/godirwalk", "gopkg.in/alecthomas/kingpin.v2"]
    try:
        with open('setup.log', 'w') as logFile:
            logFile.write("# This is an autogenerated file made by 'run.py' on {}\n".format(datetime.datetime.now()))
            logFile.write("# => DO NOT DELETE THIS FILE OR SETUP WILL BE CALLED AGAIN\n")

            logFile.flush()
            subprocess.run(["go", "version"], stdout = logFile, stderr = logFile, check=True)
            [subprocess.run(["go", "get", package], stdout = logFile, stderr = logFile, check=True) for package in dependencies]
            [subprocess.run(["go", "install", package], stdout = logFile, stderr = logFile, check=True) for package in dependencies]
            logFile.flush()

            logFile.write("\n# Setup completed on {}".format(datetime.datetime.now()))
        #end logFile
    except Exception as e:
        print(e)
        if os.path.exists('setup.log'):
            os.remove('setup.log')
#end run

def build():
    import subprocess, os
    
    # remove the previous build
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    
    process_args = ['go', 'build', '-o', output_file_name]
    subprocess.call(process_args)

    if os.path.exists(output_file_name):
        print("Built Go implementation as '{}'".format(output_file_name))
    else:
        raise AssertionError("Build failed")
#end run

def run(cmd_args):
    import subprocess
    process_args = ["./{}".format(output_file_name)] + cmd_args
    
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
        