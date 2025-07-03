# Project

This repository contains Python services and tests for generating PDF reports.

## Installation

Install the project dependencies using pip:

```bash
pip install -r requirements.txt
```


## Fonts

PDF generation requires TrueType fonts that support Cyrillic characters. Place
the necessary `.ttf` files inside a `fonts/` directory or set the
`FONT_PATH` environment variable to point to the regular font file. The
repository does not include the fonts themselves.

## Incentives and payout control

The admin interface now provides a page to record bonuses and penalties for
each employee. These incentives are stored in `bonuses_penalties.json` and can
be filtered or edited through `/api/incentives` endpoints. A separate
"Контроль выплат" dashboard helps spot suspicious payout requests with handy
filters and warning indicators.

## Running the backend

Start the API with Uvicorn:

```bash
uvicorn app.server:app --reload
```

The application mounts the compiled React admin interface from the
`admin_frontend/dist` directory.

## Building the admin frontend

Navigate to `admin_frontend` and run:

```bash
npm install
npm run build
```

The build artifacts will be placed under `admin_frontend/dist` and served by the
backend.
