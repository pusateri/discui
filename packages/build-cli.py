"""Module docstring.

Call fpm to build a package based on the type of system it's running on
"""
import sys
import subprocess
import getopt
import os

def run(cmd):
    try:
        connectionTest = subprocess.Popen([cmd], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        cstdout,cstderr = connectionTest.communicate()
        if connectionTest.returncode:
            raise Exception("lsb_release returned %s"%connectionTest.returncode)
        if cstdout:
            #print cstdout
            status = "OK"
        elif cstderr:
            #print cstderr
            status = "PROBLEM"
    except:
        e = sys.exc_info()[1]
        print "Error: %s" % e
    return cstdout

def lsb_release(arg):
    cmd = 'lsb_release ' + arg
    cstdout = run(cmd)
    return cstdout.split(':')[1].strip()

def main():
    alpha = True
    pkg_iteration = None

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:r", ["help", "iteration", "release"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-r", "--release"):
            alpha = False
        if o in ("-i", "--iteration"):
            pkg_iteration = a
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

    dist = lsb_release('-i')
    release = lsb_release('-r')
    arch = run('uname -m')
    pkg_type = 'rpm'
    pkg_name = 'python-hyp'
    pkg_version = '0.2'
    git_version = run('git rev-parse --verify --short HEAD').strip()
    maintainer = 'Tom Pusateri <pusateri@bangj.com>'
    vendor = 'bangj, LLC'
    url = 'http://hypd.info'
    description = 'DNS Hybrid Proxy Daemon User Interface'
    path = '/usr/bin'
    setup = '../hypcli/setup.py'

    if dist == 'CentOS' and float(release) < 7:
        pass
    if dist == 'Fedora':
        pass
    if dist == 'Ubuntu':
        pkg_type = 'deb'

    depends = ['python-requests', 'python-tabulate']
    cmd = "fpm -s python -t %s -n %s -v %s --maintainer '%s' --vendor '%s' --url '%s' --description '%s' " \
          % (pkg_type, pkg_name, pkg_version, maintainer, vendor, url, description)

    if pkg_iteration:
        if alpha:
            cmd = cmd + "--iteration %s.%s " % (pkg_iteration, git_version)
        else:
            cmd = cmd + "--iteration %s " % pkg_iteration
    for depend in depends:
        cmd = cmd + "-d '%s' " % depend
    cmd = cmd + setup
    print cmd
    os.system(cmd)

if __name__ == "__main__":
    sys.exit(main())
