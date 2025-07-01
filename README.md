# Project

This repository contains Python services and tests for generating PDF reports.

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
