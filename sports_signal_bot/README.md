# Sports Signal Bot

A modular, extensible, and scalable sports forecasting and signal bot built in Python. Designed to be a foundation for building complex, predictive models for football and basketball, with strong emphasis on local execution, open-source tools, and solid software engineering practices.

## Project Scope (Phase 1)
This repository represents Phase 1 of the development.

### What is done:
- Created the core project structure, packaging and dependency rules.
- Set up a clean configuration management system using `pydantic-settings`.
- Established a structured logging and exception handling base.
- Defined abstract base classes (interfaces) for data providers, features, models, notifications and orchestration.
- Created mock implementations for data providers and features to prove the architecture.
- Developed a "smoke" pipeline runner that simulates fetching data, processing features, making dummy predictions, and notifying.
- Added basic test coverage to ensure the skeleton is robust.

### What is NOT done:
- No real betting APIs integrated yet.
- No heavy ML models or training loops implemented.
- No web interface, dashboard, or browser automation.
- No live Telegram bot (only a mock stub is included).

## Installation

1. Ensure you have Python 3.11+ installed.
2. Clone the repository and navigate into the `sports_signal_bot` directory.
3. Create a virtual environment (optional but recommended):
   ```bash
   # python3 -m venv venv
   # source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package (including dev dependencies):
   ```bash
   pip install -e .[dev]
   ```
5. Copy the `.env.example` file to create your local `.env`:
   ```bash
   cp .env.example .env
   ```

## Usage

You can interact with the bot using the built-in CLI powered by Typer.

### Run the Smoke Pipeline
```bash
python -m sports_signal_bot.main smoke-run
```

### View Configuration
```bash
python -m sports_signal_bot.main show-config
```

### View Project Paths
```bash
python -m sports_signal_bot.main paths
```

## Running Tests
To ensure everything is working correctly, run the tests using `pytest`:
```bash
pytest tests/
```

## Future Phases Roadmap
- Integrate real schedule and odds APIs via the Provider interfaces.
- Build extensive feature engineering pipelines for football and basketball.
- Introduce scikit-learn / tree-based models and proper train/eval loops.
- Develop backtesting and benchmark engines to measure success using metrics beyond basic accuracy (e.g., log loss, calibration).
