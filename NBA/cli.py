"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m NBA` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``NBA.__main__`` in ``sys.modules``.

  - When you import __main__ it will get executed again (as a module) because
    there's no ``NBA.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import sys

from NBA.scripts import todays_bets
from utilities import get_lines


def main():

    class CLI:

        def __init__(self):
            parser = argparse.ArgumentParser(
                description='Tool for scraping daily lines and making predictions',
                usage='''NBA <command> [<args>]
                Commands available:
                get_lines   returns todays point spreads for NBA
                todays_bets returns predicted lines and advised bets
                '''
            )
            parser.add_argument('command', help='Subcommand to run; [todays_bets, get_lines]')

            #mostly for todays_bets, but some applicable to get_lines too
            parser.add_argument('-s', '--save', type=bool, default=True, help='To save predictions or not')
            parser.add_argument('-sb', '--sportsbook', type=str, default='DraftKings',
                                help='Define which sportsbook to pull lines from')
            parser.add_argument('-d', '--display', type=bool, default=True, help='To print the output or not')
            parser.add_argument('-t', '--threshold', type=int, default=4, help='Bet value threshold')


            args = parser.parse_args()
            if not hasattr(self, args.command):
                print('Not a valid command. Try get_lines or todays_bets')
                parser.print_help()
                exit(1)

            getattr(self, args.command)()

        def get_lines(self):
            parser = argparse.ArgumentParser(
                description='Scrapes todays lines for NBA games'
            )

            parser.add_argument('get_lines', type=str, help="Scrape lines, make bets")

            parser.add_argument('-sb', '--sportsbook', type=str, default='DraftKings',
                                help='Define which sportsbook to pull lines from')
            parser.add_argument('-d', '--display', type=bool, default=True, help='To print the output or not')

            args = parser.parse_args()

            return get_lines(sportsbook=args.sportsbook, display=args.display)

        def todays_bets(self):
            parser = argparse.ArgumentParser(
                description='Make predictions and recommend bets'
            )
            parser.add_argument('todays_bets', type=str, help="Scrape lines, make bets")
            parser.add_argument('-s', '--save', type=bool, default=True, help='To save predictions or not')
            parser.add_argument('-sb', '--sportsbook', type=str, default='DraftKings',
                                help='Define which sportsbook to pull lines from')
            parser.add_argument('-d', '--display', type=bool, default=True, help='To print the output or not')
            parser.add_argument('-t', '--threshold', type=int, default=4, help='Bet value threshold')
            args = parser.parse_args()

            return todays_bets(book=args.sportsbook, threshold=args.threshold, save=args.save, display=args.display)


    CLI()

    ####
    # parser = argparse.ArgumentParser(description='Try out')
    # parser.add_argument('command', help='subcommand to run')
    # subcommand = sys.argv[1]
    #
    # if subcommand == 'todays_bets':
    #     # parser = argparse.ArgumentParser(description='Generate daily wagers for NBA games')
    #
    #     parser.add_argument('todays_bets', type=str, help="Scrape lines, make bets")
    #     parser.add_argument('-s', '--save', type=bool, default=True, help='To save predictions or not')
    #     parser.add_argument('-sb', '--sportsbook', type=str, default='DraftKings',
    #                         help='Define which sportsbook to pull lines from')
    #     parser.add_argument('-d', '--display', type=bool, default=True, help='To print the output or not')
    #     parser.add_argument('-t', '--threshold', type=int, default=4, help='Bet value threshold')
    #     args = parser.parse_args()
    #
    #     if args.todays_bets:
    #         return todays_bets(book=args.sportsbook, threshold=args.threshold, save=args.save, display=args.display)
    #
    # if subcommand == 'get_lines':
    #     # parser = argparse.ArgumentParser(description='Generate daily wagers for NBA games')
    #
    #     # parser.add_argument('get_lines', type=str, help='Scrape todays spreads')
    #
    #     parser.add_argument('-s', '--save', type=bool, default=True, help='To save predictions or not')
    #     parser.add_argument('-sb', '--sportsbook', type=str, default='DraftKings',
    #                         help='Define which sportsbook to pull lines from')
    #     parser.add_argument('-d', '--display', type=bool, default=True, help='To print the output or not')
    #     parser.add_argument('-t', '--threshold', type=int, default=4, help='Bet value threshold')
    #
    #     args = parser.parse_args()
    #
    #     if args.get_lines:
    #         return get_lines(sportsbook=args.sportsbook, display=args.display)
