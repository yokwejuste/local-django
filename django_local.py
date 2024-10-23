#!/usr/bin/env python

import argparse
import subprocess
import sys
from django.core.management import execute_from_command_line
from local_django.translation_manager import TranslationManager


def main():
    parser = argparse.ArgumentParser(
        description="django_local - Manage translations and tasks for the Local Django project"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    translate_parser = subparsers.add_parser(
        'translate', help='Translate .po files using the configured translation service'
    )
    translate_parser.add_argument(
        '--source-lang', type=str, required=True, help='Source language code (e.g., en)'
    )
    translate_parser.add_argument(
        '--target-lang', type=str, required=True, help='Target language code (e.g., fr)'
    )
    translate_parser.add_argument(
        '--po-file', type=str,
        help='Path to the .po file to be translated. If not provided, defaults to all in LOCALE_PATHS'
    )
    translate_parser.add_argument(
        '--service', type=str, choices=['aws', 'azure'], required=True, help='Translation service to use (aws or azure)'
    )

    manage_parser = subparsers.add_parser(
        'manage', help='Run Django management commands'
    )
    manage_parser.add_argument(
        'args', nargs=argparse.REMAINDER, help='Arguments for Django management commands'
    )

    subparsers.add_parser('clean', help='Clean up build and distribution files')

    subparsers.add_parser('lint', help='Run linting checks on the project')

    subparsers.add_parser('typecheck', help='Run type checking on the project')

    args = parser.parse_args()

    if args.command == 'translate':
        handle_translate(args)
    elif args.command == 'manage':
        handle_manage(args)
    elif args.command == 'clean':
        handle_clean()
    elif args.command == 'lint':
        handle_lint()
    elif args.command == 'typecheck':
        handle_typecheck()
    else:
        parser.print_help()


def handle_translate(args):
    """
    Handle the translate command to perform translations using the specified service.
    """
    translation_manager = TranslationManager()

    print(
        f"Using {args.service.capitalize()} Translate service to translate from {args.source_lang} to {args.target_lang}...")

    try:
        if args.po_file:
            translation_manager.translate_po_file(args.po_file, args.source_lang, args.target_lang)
        else:
            translation_manager.translate_all(args.source_lang, args.target_lang)
        print(f"Translation completed successfully using {args.service.capitalize()} service!")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        sys.exit(1)


def handle_manage(args):
    """
    Handle Django management commands passed through the 'manage' subcommand.
    """
    print(f"Running Django management command: {' '.join(args.args)}")
    execute_from_command_line(['manage.py'] + args.args)


def handle_clean():
    """
    Handle the clean command to remove build and distribution files.
    """
    print("Cleaning up build and distribution files...")
    subprocess.run(["rm", "-rf", "dist", "build", "local_django.egg-info"])


def handle_lint():
    """
    Handle the lint command to run linters on the project files.
    """
    print("Running lint checks...")
    subprocess.run(["ruff", "check", "local_django"])
    subprocess.run(["ruff", "format", "--check", "local_django", "*.py"])


def handle_typecheck():
    """
    Handle the typecheck command to run type checking on the project files.
    """
    print("Running type checking...")
    subprocess.run(["mypy", "--pretty", "local_django"])


if __name__ == "__main__":
    main()
