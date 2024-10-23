# Local-Django AUTOMATIC Translation Manager

A Django package that automates the translation of `.po` files using AWS Translate or Azure Translator. This package
offers a single translation manager to manage different translation services seamlessly.

## Quick Start

### Installation

**Core Package:**

```bash
pip install local-django
```

**Optional AWS or Azure Support:**

```bash
pip install local-django[aws]
pip install local-django[azure]
```

### Configuration

Set up `TRANSLATION_MANAGER` in `settings.py` to choose a service:

```python
TRANSLATION_MANAGER = 'AWS'  # or 'AZURE'
```

Configure AWS or Azure credentials as needed.

### Usage

**Translate all `.po` files:**

```bash
python manage.py translate_po
```

**Translate a specific `.po` file:**

```bash
python manage.py translate_po path/to/your.po --source-lang en --target-lang fr
```

## Development Guidelines

### Environment Setup

1. Clone the repository and navigate to the project root.
2. Install dependencies:

    ```bash
    pip install -r requirements/base.txt
    ```

3. Install development dependencies:

    ```bash
    pip install -r requirements/dev.txt
    ```

### Testing & Linting

**Run Tests:**

```bash
make test
```

**Lint the Project:**

```bash
make lint
```

### Contributing

- Fork the repository.
- Create a new branch.
- Make your changes, run tests, and submit a pull request.

## License

MIT License. See [LICENSE](./LICENSE) for details.
