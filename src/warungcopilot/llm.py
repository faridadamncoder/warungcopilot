"""Klien opsional Meta Model API.

Dipakai HANYA kalau MODEL_API_KEY diisi lewat environment.
Tidak ada key yang ditulis di repo ini, dan modul ini tidak pernah
dipanggil oleh demo.py supaya demo tetap jalan tanpa key.
"""

import os


def chat(message, model=None, base_url=None, api_key=None):
    """Satu panggilan chat ke Meta Model API (OpenAI-compatible)."""
    api_key = api_key or os.environ.get("MODEL_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "MODEL_API_KEY belum diisi. Isi di .env, jangan commit file itu."
        )
    from openai import OpenAI

    client = OpenAI(
        base_url=base_url or os.environ.get("MODEL_BASE_URL", "https://api.meta.ai/v1"),
        api_key=api_key,
    )
    resp = client.chat.completions.create(
        model=model or os.environ.get("MODEL_NAME", "muse-spark-1.3"),
        messages=[{"role": "user", "content": message}],
    )
    return resp.choices[0].message.content
