import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.schemas.payout import Payout


def test_payout_json_fields_match_schema():
    # use example data shipped with the repo
    path = Path('advance_requests.example.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    fields = set(Payout.model_fields.keys())
    required = fields - {'id', 'timestamp'}
    for item in data:
        assert required.issubset(item.keys())
        assert set(item.keys()).issubset(fields)
