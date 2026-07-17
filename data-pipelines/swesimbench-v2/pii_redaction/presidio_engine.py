"""Presidio NER + context-validated redaction (Joe steps 2–4).

Uses CPU spaCy ``en_core_web_sm`` (no GPU on this host). Joe's SLURM path uses
``en_core_web_trf`` + GPU — same validators / code-fence guard / entity set.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .code_spans import code_spans, in_code
from .validators import REDACT_ENTITIES, THRESHOLDS, VALIDATORS

_ANALYZER = None
_ANONYMIZER = None


def _get_engines(model_name: str = "en_core_web_sm"):
    global _ANALYZER, _ANONYMIZER
    if _ANALYZER is not None:
        return _ANALYZER, _ANONYMIZER
    from presidio_analyzer import AnalyzerEngine
    from presidio_analyzer.nlp_engine import NlpEngineProvider
    from presidio_anonymizer import AnonymizerEngine

    nlp_config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": model_name}],
    }
    provider = NlpEngineProvider(nlp_configuration=nlp_config)
    nlp_engine = provider.create_engine()
    _ANALYZER = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
    _ANONYMIZER = AnonymizerEngine()
    return _ANALYZER, _ANONYMIZER


def analyze(text: str, model_name: str = "en_core_web_sm", max_chars: int = 24_000) -> list[Any]:
    if not text or not text.strip():
        return []
    analyzer, _ = _get_engines(model_name)
    # Cap pathological megapastes — Presidio/spaCy can thrash on huge blobs.
    sample = text if len(text) <= max_chars else text[:max_chars]
    try:
        return analyzer.analyze(text=sample, entities=list(REDACT_ENTITIES), language="en")
    except Exception as exc:  # noqa: BLE001
        print(f"[presidio] analyze failed: {exc!r}", flush=True)
        return []


def redact(
    text: str,
    analyzer_results: list[Any] | None = None,
    document_freq: dict[str, dict[str, int]] | None = None,
    model_name: str = "en_core_web_sm",
):
    """Apply Joe-style context-validated Presidio redaction.

    Returns (new_text, Counter of entity redactions).
    """
    if not text:
        return text, Counter()
    results = analyzer_results if analyzer_results is not None else analyze(text, model_name)
    if not results:
        return text, Counter()

    max_chars = 24_000
    # Work on the same truncated view used for analysis when needed.
    working = text if len(text) <= max_chars else text[:max_chars]
    spans = code_spans(working)
    keep = []
    hits: Counter[str] = Counter()
    for r in results:
        entity = r.entity_type
        if entity not in REDACT_ENTITIES:
            continue
        word = working[r.start : r.end]
        if in_code(r.start, r.end, spans):
            continue
        word_l = word.strip().lower()
        if document_freq is not None:
            thresh = THRESHOLDS.get(entity, 10)
            if document_freq.get(entity, {}).get(word_l, 0) >= thresh:
                continue
        ctx_local = working[max(0, r.start - 20) : r.start]
        validator = VALIDATORS.get(entity)
        if validator is not None and validator(word, ctx_local, working):
            continue
        keep.append(r)
        hits[f"presidio_{entity}"] += 1

    if not keep:
        return text, Counter()

    _, anonymizer = _get_engines(model_name)
    from presidio_anonymizer.entities import OperatorConfig

    operators = {
        e: OperatorConfig("replace", {"new_value": f"<PRESIDIO_ANONYMIZED_{e}>"})
        for e in REDACT_ENTITIES
    }
    res = anonymizer.anonymize(text=working, analyzer_results=keep, operators=operators)
    if len(text) <= max_chars:
        return res.text, hits
    # Only the prefix was analyzed; stitch back the untouched suffix.
    return res.text + text[max_chars:], hits


def update_document_freq(
    document_freq: dict[str, dict[str, int]],
    text: str,
    analyzer_results: list[Any],
) -> None:
    """Accumulate per-entity document frequencies (session-level caller should
    de-dupe words per session before calling)."""
    for r in analyzer_results:
        entity = r.entity_type
        if entity not in REDACT_ENTITIES:
            continue
        word = text[r.start : r.end].strip().lower()
        if not word:
            continue
        document_freq.setdefault(entity, defaultdict(int))
        document_freq[entity][word] += 1
