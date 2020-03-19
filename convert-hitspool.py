#!/usr/bin/env python
#
# Reduce hits from a file or HitSpool directory to only the SimpleHits
# which would be sent to the local triggers

import os
import sys

# main class being run
MAIN_CLASS = "icecube.daq.testbed.ConvertHitSpool"

# special arguments for JVM
JAVA_ARGS = ""

# required jar files from subprojects and Maven repository
SUBPROJECT_PKGS = ("daq-common", "splicer", "payload", "daq-io", "juggler",
                   "trigger", "trigger-testbed")
REPO_PKGS = [("log4j", "log4j", "1.2.17"),
             ("commons-logging", "commons-logging", "1.1")]


def find_dash_directory():
    """
    Try to locate pDAQ's `dash` directory
    Throw SystemExit if it cannot be found
    """
    if "PDAQ_HOME" in os.environ:
        return os.path.join(os.environ["PDAQ_HOME"], "dash")

    for path in ("../dash", "dash"):
        if os.path.exists(path):
            return path

    raise SystemExit("Cannot find pDAQ's 'dash' directory")


sys.path.append(find_dash_directory())


from RunJava import JavaRunner


if __name__ == "__main__":
    runner = JavaRunner(MAIN_CLASS, SUBPROJECT_PKGS, REPO_PKGS)

    try:
        if isinstance(JAVA_ARGS, list) or isinstance(JAVA_ARGS, tuple):
            jargs = JAVA_ARGS
        else:
            jargs = (JAVA_ARGS, )
    except NameError:
        jargs = None

    debug = "DEBUG" in os.environ

    rundata = runner.run(None, jargs, sys.argv[1:], debug=debug)
    if rundata.returncode is not None and rundata.returncode != 0:
        raise SystemExit(rundata.returncode)