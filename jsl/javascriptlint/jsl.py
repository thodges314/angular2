#!/usr/bin/python
# vim: ts=4 sw=4 expandtab
import fnmatch
import functools
import os
import sys
import unittest
from optparse import OptionParser

import conf
import fs
import htmlparse
import jsparse
import jsengine.parser
import lint
import util
import version

_lint_results = {
    'warning': 0,
    'errors': 0
}

def _dump(paths, encoding):
    for path in paths:
        script = fs.readfile(path, encoding)
        jsparse.dump_tree(script)

def _lint_warning(conf_, path, line, col, msg_type, errname, errdesc):
    assert msg_type in ('warning', 'error')
    _lint_results[msg_type] += 1
    print util.format_error(conf_['output-format'], path, line, col,
                                  errname, errdesc)

def _lint(paths, conf_, printpaths, encoding):
    lint.lint_files(paths, functools.partial(_lint_warning, conf_), encoding,
                    conf=conf_, printpaths=printpaths)

def _resolve_paths(path, recurse):
    # Build a list of directories
    paths = []

    dir, pattern = os.path.split(path)
    for cur_root, cur_dirs, cur_files in os.walk(dir):
        paths.extend(os.path.join(cur_root, file) for file in \
                     fnmatch.filter(cur_files, pattern))
        if not recurse:
            break

    # If no files have been found, return the original path/pattern. This will
    # force an error to be thrown if no matching files were found.
    return paths or [path]

def printlogo():
    print "JavaScript Lint %s" % version.version
    print "Developed by Matthias Miller (http://www.JavaScriptLint.com)"

def _profile_enabled(func, *args, **kwargs):
    import tempfile
    import hotshot
    import hotshot.stats
    handle, filename = tempfile.mkstemp()
    profile = hotshot.Profile(filename)
    profile.runcall(func, *args, **kwargs)
    profile.close()
    stats = hotshot.stats.load(filename)
    stats = stats.sort_stats("time")
    stats.print_stats()
def _profile_disabled(func, *args, **kwargs):
    func(*args, **kwargs)

def _main():
    parser = OptionParser(usage="%prog [options] [files]")
    add = parser.add_option
    add("--conf", dest="conf", metavar="CONF",
        help="set the conf file")
    add("--profile", dest="profile", action="store_true", default=False,
        help="turn on hotshot profiling")
    add("--recurse", dest="recurse", action="store_true", default=False,
        help="recursively search directories on the command line")
    if os.name == 'nt':
        add("--disable-wildcards", dest="wildcards", action="store_false",
            default=True, help="do not resolve wildcards in the command line")
    else:
        add("--enable-wildcards", dest="wildcards", action="store_true",
            default=False, help="resolve wildcards in the command line")
    add("--dump", dest="dump", action="store_true", default=False,
        help="dump this script")
    add("--unittest", dest="unittest", action="store_true", default=False,
        help="run the python unittests")
    add("--quiet", dest="verbosity", action="store_const", const=0,
        help="minimal output")
    add("--verbose", dest="verbosity", action="store_const", const=2,
        help="verbose output")
    add("--nologo", dest="printlogo", action="store_false", default=True,
        help="suppress version information")
    add("--nofilelisting", dest="printlisting", action="store_false",
        default=True, help="suppress file names")
    add("--nosummary", dest="printsummary", action="store_false", default=True,
        help="suppress lint summary")
    add("--help:conf", dest="showdefaultconf", action="store_true", default=False,
        help="display the default configuration file")
    add("--encoding", dest="encoding", metavar="ENCODING", default="utf-8",
        help="encoding for input file(s)")
    parser.set_defaults(verbosity=1)
    options, args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    if options.showdefaultconf:
        print conf.DEFAULT_CONF
        sys.exit()

    if options.printlogo:
        printlogo()

    conf_ = conf.Conf()
    if options.conf:
        try:
            conf_.loadfile(options.conf)
        except conf.ConfError, error:
            _lint_warning(conf_, error.path, error.lineno, 0, 'error', 'conf_error',
                          unicode(error))

    profile_func = _profile_disabled
    if options.profile:
        profile_func = _profile_enabled

    if options.unittest:
        suite = unittest.TestSuite();
        for module in [conf, htmlparse, jsengine.parser, jsparse, lint, util]:
            suite.addTest(unittest.findTestCases(module))

        runner = unittest.TextTestRunner(verbosity=options.verbosity)
        runner.run(suite)

    paths = []
    for recurse, path in conf_['paths']:
        paths.extend(_resolve_paths(path, recurse))
    for arg in args:
        if options.wildcards:
            paths.extend(_resolve_paths(arg, options.recurse))
        elif options.recurse and os.path.isdir(arg):
            paths.extend(_resolve_paths(os.path.join(arg, '*'), True))
        else:
            paths.append(arg)
    if options.dump:
        profile_func(_dump, paths, options.encoding)
    else:
        profile_func(_lint, paths, conf_, options.printlisting, options.encoding)

    if options.printsummary:
        print '\n%i error(s), %i warnings(s)' % (_lint_results['error'],
                                                 _lint_results['warning'])

    if _lint_results['error']:
        sys.exit(3)
    if _lint_results['warning']:
        sys.exit(1)
    sys.exit(0)

def main():
    try:
        _main()
    except KeyboardInterrupt:
        raise SystemExit(130)

if __name__ == '__main__':
    main()

