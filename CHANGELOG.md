# Changelog

## [0.0.1] - 2024-10-10

### Initial Release
- Created the initial version of the `local-django` package.
- Implemented `TranslationManager` to support AWS Translate and Azure Translator.
- Added `django_local` command-line interface with the following subcommands:
  - `translate`: Translate `.po` files using the configured translation service.
  - `manage`: Run Django management commands.
  - `clean`: Clean up build and distribution files.
  - `lint`: Run linting checks on the project files.
  - `typecheck`: Run type checking on the project files.
