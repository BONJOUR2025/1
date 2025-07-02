import json
from pathlib import Path


def test_config_json_has_basic_keys():
    path = Path('config.json')
    if not path.exists():
        path.write_text('{}', encoding='utf-8')
    data = json.loads(path.read_text(encoding='utf-8'))
    for key in ['company_name', 'default_currency', 'payout_types']:
        assert key in data
