# NanoMan

**Offline API Testing Client**

NanoMan is a lightweight, privacy-focused API testing tool. No cloud, no bloat, just requests. Part of the **Nano Product Family**.

![Python](https://img.shields.io/badge/Made%20with-Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Features

* **Offline First:** Works without internet connection for local APIs
* **Privacy Focused:** No telemetry, no cloud, your data stays local
* **Full HTTP Support:** GET, POST, PUT, PATCH, DELETE methods
* **JSON Pretty-Print:** Automatic formatting of JSON responses
* **Custom Headers:** Set any headers for your requests
* **Threaded Requests:** UI never freezes, even on slow connections
* **Security Focused:** Strict URL validation (HTTP/HTTPS only)

## Requirements

* Python 3.8+
* Dependencies: `customtkinter`, `requests`

## Installation

```bash
# Clone repository
git clone https://github.com/goAuD/NanoMan.git
cd NanoMan

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Usage

1. Select HTTP method (GET, POST, PUT, PATCH, DELETE)
2. Enter API URL
3. (Optional) Add request body JSON in "Request Body" tab
4. (Optional) Add custom headers in "Headers" tab
5. Click **SEND** or press **Enter**

## Project Structure

```
NanoMan/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── src/
│   ├── __init__.py
│   ├── logic.py         # Business logic (API, validation)
│   └── ui.py            # CustomTkinter UI
└── tests/
    ├── __init__.py
    └── test_logic.py    # Unit tests (9 tests)
```

## Security

| Threat | Prevention |
|--------|------------|
| XSS via URL | Only `http://` and `https://` allowed |
| JavaScript injection | `javascript:` URLs rejected |
| File access | `file://` URLs rejected |
| Request hanging | 10 second timeout |
| UI freeze | Threaded requests |

## Running Tests

```bash
python -c "import sys; sys.path.insert(0, '.'); from tests.test_logic import *; import unittest; unittest.main(module='tests.test_logic', verbosity=2, exit=False)"
```

## Part of Nano Product Family

This tool uses the [Nano Design System](https://github.com/goAuD/NanoServer/blob/main/DESIGN_SYSTEM.md) for consistent styling across lightweight developer tools.

## License

MIT License
