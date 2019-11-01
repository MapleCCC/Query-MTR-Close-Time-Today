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

from query.query import brute_force_query, normal_mode_query

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
    parser.add_argument("-d", "--debug", action="store_true",
                        default=False, help="Run in debug mode")
    parser.add_argument(
        "--fall-back",
        action="store_true",
        default=False,
        help="Decide whether to resume with normal mode query after brute force query failed")
    group.add_argument(
        "--fire-browser",
        action="store_true",
        default=False,
        help="When query fails, open the train service info "
        "announcement website in browser instead.")
    group.add_argument(
        "--register-mail-notifier",
        type=str,
        nargs="?",
        metavar="EMAIL_ADDRESS",
        default=None,
        help="Register an entry in scheduler for  when update is detected, send an email to EMAIL_ADDR")
    # parser.add_argument("-q", "--quiet", action="store_true",
    #                     default=False, help="Run in quiet mode")
    # parser.add_argument("--locale", type=str,
    #                     default="zh-cn", help="Set the locale")


def query(args):

    def handle_brute_force_query_failure():
        if args.fall_back:
            print("Brute-force strategy failed. Try normal mode instead.")
        else:
            if args.debug:
                raise RuntimeError("Brute-force strategy failed")
            else:
                # `from None` suppresses exception chaining
                raise RuntimeError("Brute-force query failed") from None

    def handle_normal_mode_query_failure():
        if args.fire_browser:
            print("Normal mode query failed. Open the web page in browser instead.")
            webbrowser.open_new_tab(MTR_TSI_ANNOUNCEMENT_URL)
        else:
            if args.debug:
                raise RuntimeError("Normal mode query failed")
            else:
                # `from None` suppresses exception chaining
                raise RuntimeError("Normal mode query failed") from None

    if not args.debug:
        # this clean trick also has desirable side effect that exception
        # chaining is suppressed.
        sys.excepthook = lambda exctype, exc, traceback: print(
            f"{exctype.__name__}: {exc}")

    if args.brute_force:
        # quick and dirty query
        try:
            return brute_force_query(args.verbose)
        except:
            handle_brute_force_query_failure()

    try:
        return normal_mode_query(args.verbose)
    except:
        handle_normal_mode_query_failure()


def main():
    parser = argparse.ArgumentParser(
        description="Query when will MTR close today.")
    initialize_argparser(parser)
    args = parser.parse_args()

    if args.register_mail_notifier:
        raise NotImplementedError
    else:
        # Run as CLI mode
        result = query(args)
        print(result)


if __name__ == '__main__':
    main()
