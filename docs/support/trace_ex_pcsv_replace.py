# trace_ex_pcsv_replace.py
# Copyright (c) 2013-2017 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,W0212

import docs.support.trace_support


def trace_module(no_print=False):
    """ Trace pcsv replace module exceptions """
    mname = 'replace'
    fname = 'pcsv'
    module_prefix = 'pcsv.{0}.'.format(mname)
    callable_names = (
        mname,
    )
    return docs.support.trace_support.run_trace(
        mname, fname, module_prefix, callable_names, no_print
    )


if __name__ == '__main__':
    trace_module()
