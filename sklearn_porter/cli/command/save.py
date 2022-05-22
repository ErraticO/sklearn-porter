from argparse import RawTextHelpFormatter, _SubParsersAction
from logging import DEBUG
from pathlib import Path
from textwrap import dedent
from typing import Dict

# sklearn-porter
from sklearn_porter import Estimator, options
from sklearn_porter.cli.common import arg_debug, arg_help, arg_skip_warnings
from sklearn_porter.cli.utils import load_model
from sklearn_porter.language import LANGUAGES


def config(sub_parser: _SubParsersAction):

    header = 'The subcommand `save` transpiles a trained ' \
             'estimator to a specific programming language ' \
             'and saves the result.'
    footer = dedent(
        """
        Examples:
          `porter save model.pkl --language js --template attached`
          `porter save model.pkl --directory /tmp --skip-warnings`
          `porter save model.pkl -l js -t exported --directory /tmp --skip-warnings`
    """
    )

    parser = sub_parser.add_parser(
        'save',
        description=header,
        help='Port a trained estimator and save the result.',
        epilog=footer,
        formatter_class=RawTextHelpFormatter,
        add_help=False,
    )
    for group in parser._action_groups:
        group.title = str(group.title).capitalize()

    parser.add_argument(
        'model', type=str, help='Path to an exported estimator.'
    )
    parser.add_argument(
        '-l',
        '--language',
        type=str,
        required=False,
        choices=LANGUAGES.keys(),
        help='The name of the programming language.'
    )
    parser.add_argument(
        '-t',
        '--template',
        type=str,
        required=False,
        choices=['attached', 'combined', 'exported'],
        help='The name of the template.'
    )
    parser.add_argument(
        '--directory',
        type=str,
        required=False,
        help='The directory where the generated files will be saved.'
    )

    for fn in (arg_skip_warnings, arg_debug, arg_help):
        fn(parser)

    parser.set_defaults(func=main)


def main(args: Dict, silent: bool = False):
    if args.get('debug'):
        options['logging.level'] = DEBUG

    path = Path(args.get('model'))
    mdl = load_model(path, args.get('skip_warnings', False))
    est = Estimator(mdl)

    if args.get('language'):
        est.language = args.get('language')

    if args.get('template'):
        est.template = args.get('template')

    directory = args.get('directory')
    if not directory:
        directory = Path.cwd()
    paths = est.save(directory=directory)

    if not isinstance(paths, tuple):
        paths = (paths, )

    out = ['Saved files:']
    for p in paths:
        out.append('  ' + str(p))
    out = '\n'.join(out)

    if not silent:
        print(out)

    return out
