# Calculate.

A clean, responsive calculator powered by a small FastAPI backend. Use the on-screen keypad or your keyboard to work through everyday arithmetic.

## Features

- Responsive calculator interface for desktop and mobile
- Mouse, touch, and keyboard input
- Addition, subtraction, multiplication, division, modulo, and unary signs
- Parentheses for grouping expressions
- Recent results for the current page session
- Server-side expression evaluation with Python's AST (without `eval`)
- Clear feedback for invalid calculations and division by zero
- Interactive API documentation from FastAPI

## Preview

The calculator is served by the FastAPI app at the root URL (`/`). The frontend is a standalone HTML file in `static/index.html`.

## Requirements

- Python 3.10 or newer
- pip

Python packages are listed in [`requirements.txt`](requirements.txt).

## Run locally

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks environment activation, run the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000) in your browser. To use Uvicorn's reload mode during development:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 3000
```

## API

Calculate an expression by sending JSON to `POST /calculate`:

```bash
curl -X POST http://127.0.0.1:3000/calculate \
  -H "Content-Type: application/json" \
  -d "{\"expression\":\"(12 + 8) * 3 / 2\"}"
```

Successful response:

```json
{"result": 30.0}
```

Expressions are limited to 200 characters. The API accepts numeric constants, parentheses, `+`, `-`, `*`, `/`, `%`, and unary `+` and `-`. Unsupported syntax and division by zero return HTTP 400.

- `GET /` — calculator frontend
- `POST /calculate` — evaluate an expression
- `GET /docs` — interactive Swagger API documentation
- `GET /redoc` — ReDoc API documentation
- `GET /contact` — simple contact/status response

## Project structure

```text
.
├── main.py             # FastAPI application and safe calculator evaluator
├── requirements.txt    # Python dependencies
└── static/
    └── index.html      # Responsive calculator frontend
```

## License

No license has been specified yet. All rights reserved unless the repository owner adds a license.
