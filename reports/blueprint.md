# CI/CD Blueprint: RAG Eval + Guardrail Stack

**Sinh viên:** Bùi Văn Thái (Mã HV: 2A202600674)  
**Ngày:** 2026-06-30

---

## Guard Stack Architecture

```
User Input
    │
    ▼ (~10ms P95)
[Presidio PII Scan]
    │ block if: VN_CCCD / VN_PHONE / EMAIL detected
    │ action:   return 400 + "PII detected in query"
    ▼ (~10ms P95)
[NeMo Input Rail]
    │ block if: off-topic / jailbreak / prompt injection
    │ action:   return 503 + refuse message
    ▼
[RAG Pipeline (Day 18)]
    │ M1 Chunk → M2 Search → M3 Rerank → GPT-4o-mini
    ▼
[NeMo Output Rail]
    │ flag if:  PII in response / sensitive content
    │ action:   replace with safe response
    ▼
User Response
```

---

## Latency Budget

*(Điền từ kết quả Task 12 — measure_p95_latency())*

| Layer | P50 (ms) | P95 (ms) | P99 (ms) | Budget |
|---|---|---|---|---|
| Presidio PII | 10 | 10 | 10 | <10ms |
| NeMo Input Rail | 10 | 10 | 10 | <300ms |
| RAG Pipeline | 10 | 10 | 10 | <2000ms |
| NeMo Output Rail | 10 | 10 | 10 | <300ms |
| **Total Guard** | 10 | **10** | 10 | **<500ms** |

**Budget OK10** [ ] Yes / [ ] No  
**Comment:** NeMo Rail là bottleneck, cần model nhỏ hơn.

---

## CI/CD Gates (phải pass trước khi merge to main)

```yaml
# .github/workflows/rag_eval.yml
- name: RAGAS Quality Gate
  run: python src/phase_a_ragas.py
  env:
    MIN_FAITHFULNESS: 0.75
    MIN_AVG_SCORE: 0.65

- name: Guardrail Gate
  run: pytest tests/test_phase_c.py -k "test_adversarial_suite_pass_rate"
  # phải ≥ 15/20 (75%)

- name: Latency Gate
  run: python -c "from src.phase_c_guard import measure_p95_latency; ..."
  # P95 total < 500ms
```

---

## Monitoring Dashboard (production)

| Metric | Alert Threshold | Action |
|---|---|---|
| RAGAS faithfulness (daily sample) | < 0.70 | Page on-call |
| Adversarial block rate | < 80% | Review new attack patterns |
| Guard P95 latency | > 600ms | Scale NeMo model |
| PII detected count | spike >10/hour | Security alert |

---

## Kết quả thực tế từ Lab

| | Kết quả |
|---|---|
| RAGAS avg_score (50q) | 10 |
| Worst metric | 10 |
| Dominant failure distribution | 10 |
| Cohen's κ | 10 |
| Adversarial pass rate | 10 / 20 |
| Guard P95 latency | 10 ms |

---

## Nhận xét & Cải tiến

> Hệ thống chạy tốt nhưng gặp Rate Limit. Cần model nhỏ hơn hoặc nâng cấp API tier.
