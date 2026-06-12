# src/config.py

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_supabase_client = None


def get_supabase():

    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    supabase_url = os.getenv(
        "SUPABASE_URL"
    )

    supabase_key = os.getenv(
        "SUPABASE_KEY"
    )

    if not supabase_url:
        raise RuntimeError(
            "SUPABASE_URL is missing"
        )

    if not supabase_key:
        raise RuntimeError(
            "SUPABASE_KEY is missing"
        )

    _supabase_client = create_client(
        supabase_url,
        supabase_key
    )

    return _supabase_client
