from fastapi.testclient import TestClient

from app.main import app
from app.services.fab_data import build_basic_stats, get_filtered_wafers, get_latest_wafers

client = TestClient(app)


def test_uc1_latest_wafers_chat_and_query():
    res = client.post('/api/chat', json={'message': '최근 wafer 10개 알려줘'})
    assert res.status_code == 200
    payload = res.json()
    assert payload['tool_results']['graph']['nodes']
    assert payload['tool_results']['table']
    assert '최신 wafer' in payload['message']

    query_res = client.post('/api/query/cypher', json={'query': '// uc1 latest wafers', 'parameters': {'limit': 3}})
    assert query_res.status_code == 200
    body = query_res.json()
    assert body['row_count'] == 3
    assert len(body['result']['raw']) == 3


def test_uc2_filtered_stats_sample_path():
    rows, source = get_filtered_wafers(status='hold', limit=10)
    assert source in {'sample', 'postgres'}
    assert rows
    assert all(row['status'].lower() == 'hold' for row in rows)

    stats = build_basic_stats(rows)
    assert stats['row_count'] == len(rows)
    assert stats['metric_value']['avg'] >= stats['metric_value']['min']

    res = client.post('/api/chat', json={'message': 'hold 상태 wafer만 필터해서 통계 보여줘'})
    assert res.status_code == 200
    payload = res.json()
    assert payload['tool_results']['chart']['chartType'] == 'bar'
    assert payload['tool_results']['table']
    assert '상태 분포' in payload['message']


def test_uc3_group_exploration_endpoint():
    res = client.post('/api/query/cypher', json={'query': '// uc3 same period DOE exploration', 'parameters': {'mode': 'uc3', 'group_by': 'lot_id'}})
    assert res.status_code == 200
    payload = res.json()
    labels = [label for node in payload['result']['nodes'] for label in node['labels']]
    assert 'Exploration' in labels
    assert payload['result']['raw']

    chat_res = client.post('/api/chat', json={'message': '동일 기간 lot 그룹 탐색 보여줘'})
    assert chat_res.status_code == 200
    chat_payload = chat_res.json()
    assert '동일 기간 그룹 탐색' in chat_payload['message']
    assert chat_payload['tool_results']['graph']['nodes']


def test_service_latest_rows_limit_is_bounded():
    rows, _source = get_latest_wafers(limit=999)
    assert 1 <= len(rows) <= 50
