import argparse
import os
import sys
import textwrap


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


parser = argparse.ArgumentParser()


COMMANDS = {}


###########################################################################
#                                resetdb                                  #
###########################################################################


def resetdb(args):
    setup_db = 'otree migrate --traceback'

    app = args.app[0]

    reset_db = 'heroku pg:reset DATABASE --confirm {}'.format(app)
    os.system(reset_db)

    heroku_run_command = 'heroku run {} --app {}'

    heroku_setup_db = heroku_run_command.format(setup_db, app)
    os.system(heroku_setup_db)

resetdb.parser = argparse.ArgumentParser(description='resetdb')
resetdb.parser.add_argument('resetdb', nargs=1)
resetdb.parser.add_argument(
    'app', nargs=1,
    help="""
        Will reset the DB on the named Heroku app.
        For example, if your URL is myapp.herokuapp.com, you would do:
        Example: ./otree-heroku resetdb myapp
    """)

COMMANDS['resetdb'] = resetdb


###########################################################################
#                                  help                                   #
###########################################################################


def show_help(args):
    if args.subcommand in COMMANDS:
        # If there was a argument given after 'help', then show the help
        # message for this command.
        if args.subcommand in COMMANDS:
            command = COMMANDS[args.subcommand]
            print(command.parser.format_help())
            return

    MESSAGE = """\
        Usage: {script_name} subcommand [options] [args]

        Call this script with a command name as first argument to execute this
        command. The deployment commands assist you in deploying your oTree
        instance to heroku.

        Type '{script_name} help <subcommand>' for help on a specific
        subcommand.

        Available subcommands:

        {deployment_commands}
    """
    MESSAGE = textwrap.dedent(MESSAGE)

    deployment_commands = sorted(COMMANDS.keys())
    deployment_commands = [(' ' * 4) + cmd for cmd in deployment_commands]
    deployment_commands = '\n'.join(deployment_commands)

    print(MESSAGE.format(
        deployment_commands=deployment_commands,
        script_name=os.path.basename(sys.argv[0])))


show_help.parser = argparse.ArgumentParser(description='help')
show_help.parser.add_argument('help', nargs=1)
show_help.parser.add_argument('subcommand', nargs='?')

COMMANDS['help'] = show_help


###########################################################################
#                                  main                                   #
###########################################################################


parser.add_argument('subcommand', nargs=1, choices=COMMANDS.keys())


def execute_from_command_line(argv):
    arguments = sys.argv[1:]
    args, unknown_args = parser.parse_known_args(arguments)
    command_name = args.subcommand[0]
    command = COMMANDS[command_name]
    command_args = command.parser.parse_args(arguments)
    command(command_args)
