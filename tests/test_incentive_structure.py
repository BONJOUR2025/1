import json
from pathlib import Path

from app.schemas.incentive import Incentive


def test_incentive_json_matches_schema():
    path = Path('bonuses_penalties.json')
    if not path.exists():
        path.write_text('[]', encoding='utf-8')
    data = json.loads(path.read_text(encoding='utf-8'))
    fields = set(Incentive.model_fields.keys())
    required = fields - {'id', 'locked'}
    for item in data:
        assert required.issubset(item.keys())
        assert set(item.keys()).issubset(fields)
