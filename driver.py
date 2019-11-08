#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
Script for query when will MTR close today.

Driver should be registered with operating system's scheduler.
"""

__author__ = 'MapleCCC, <littlelittlemaple@gmail.com>'

import argparse
import sys
import webbrowser

from query import brute_force_query, normal_mode_query
from utils import get_default_email_address

MTR_TSI_ANNOUNCEMENT_URL = 'http://www.mtr.com.hk/alert/tsi_simpletxt_title_tc.html'


def initialize_argparser(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-b",
        "--brute-force",
        action="store_true",
        default=False,
        help="Find the close time with brute-force strategy. "
        "Script runs faster and consumes less memory, "
        "but the result might be less reliable.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        default=False, help="Increase verbosity")
    parser.add_argument(
        "-d",
        "--debug",
        dest="enabled_debug_mode",
        action="store_true",
        default=False,
        help="Run in debug mode")
    parser.add_argument(
        "--fall-back",
        dest="enabled_fall_back",
        action="store_true",
        default=False,
        help="Decide whether to resume with normal mode query after brute force query failed")
    group.add_argument(
        "--fire-browser",
        dest="enabled_fire_browser",
        action="store_true",
        default=False,
        help="When query fails, open the train service info "
        "announcement website in browser instead.")
    group.add_argument(
        "--register-mail-notifier",
        nargs="?",
        metavar="EMAIL_ADDRESS",
        dest="email_address",
        default=None,
        const=get_default_email_address(),
        help="Register an entry in scheduler, periodically run "
             "and detect update, send a notification email to EMAIL_ADDRESS.")
    # parser.add_argument("-q", "--quiet", action="store_true",
    #                     default=False, help="Run in quiet mode")
    # parser.add_argument("--locale", type=str,
    #                     default="zh-cn", help="Set the locale")


def query(args) -> str:

    def handle_brute_force_query_failure(e: BaseException):
        if args.enabled_fall_back:
            if args.verbose:
                print("Brute-force strategy failed. Try normal mode instead.")
            # get out of failure handler, return flow of control
            # to main function to propogate to normal mode query
            return

        if args.enable_debug_mode:
            raise RuntimeError("Brute-force strategy failed")
        else:
            # `from None` suppresses exception chaining
            raise RuntimeError("Brute-force query failed") from None

    def handle_normal_mode_query_failure(e: BaseException):
        if args.enabled_fire_browser:
            print("Normal mode query failed. Open the web page in browser instead.")
            webbrowser.open_new_tab(MTR_TSI_ANNOUNCEMENT_URL)
            return

        if args.enabled_debug_mode:
            raise RuntimeError("Normal mode query failed")
        else:
            # `from None` suppresses exception chaining
            raise RuntimeError("Normal mode query failed") from None

    if not args.enabled_debug_mode:
        # this clean trick also has desirable side effect that exception
        # chaining is suppressed.
        sys.excepthook = lambda exctype, exc, traceback: print(
            f"{exctype.__name__}: {exc}")

    if args.brute_force:
        # quick and dirty query
        try:
            return brute_force_query(args.verbose)
        except BaseException as e:
            handle_brute_force_query_failure(e)

    try:
        return normal_mode_query(args.verbose)
    except BaseException as e:
        handle_normal_mode_query_failure(e)


def main(args: list = sys.argv):
    parser = argparse.ArgumentParser(
        description="Query when will MTR close today.")
    initialize_argparser(parser)
    args = parser.parse_args(args[1:])

    if args.email_address:
        raise NotImplementedError
    else:
        # Run as CLI mode
        result = query(args)
        print(result)


if __name__ == '__main__':
    sys.exit(main())
