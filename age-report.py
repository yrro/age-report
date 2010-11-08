#!/usr/bin/python

import argparse
import time
import spwd
import traceback

import action_meta
import actions

def safe (f, *args, **kwargs):
    try:
        return f (*args, **kwargs)
    except:
        traceback.print_exc ()

if __name__ == '__main__':
    p = argparse.ArgumentParser ()
    sp = p.add_subparsers ()

    for k, v in action_meta.registry.items ():
        if v is action_meta.action:
            continue
        ap = sp.add_parser (k, help=v.help)
        ap.set_defaults (klass=v)
        v.add_arguments (ap)

    args = p.parse_args ()

    action = args.klass (args)
    today = int (time.time () / 86400)

    for a in spwd.getspall ():
        until_disable = a.sp_expire - today
        until_expire = a.sp_max - today + a.sp_lstchg
        until_warn = until_expire - a.sp_warn
        until_inactive = until_expire + a.sp_inact

        if until_disable <= 0 and a.sp_expire >= 0:
            safe (action.disabled, a)

        elif a.sp_lstchg == 0:
            safe (action.force_expired, a)

        elif until_inactive <= 0:
            safe (action.inactive, a)

        elif until_expire <= 0:
            safe (action.expired, a, until_inactive)

        elif until_warn <= 0:
            safe (action.warn, a, until_expire)

        else:
            safe (action.ok, a)
