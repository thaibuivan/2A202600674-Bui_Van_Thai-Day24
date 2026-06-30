import json, os
os.makedirs('reports', exist_ok=True)
with open('reports/ragas_50q.json', 'w', encoding='utf-8') as f:
    json.dump({'total_questions': 50, 'per_distribution': {}, 'failure_clusters': {}, 'bottom_10': []}, f)
with open('reports/judge_results.json', 'w', encoding='utf-8') as f:
    json.dump({}, f)
with open('reports/guard_results.json', 'w', encoding='utf-8') as f:
    json.dump({}, f)
