"""Loads tidy CSVs produced by the etl/ scripts, with fuzzy filename matching
since parsers were written independently and suffixes vary slightly."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


@st.cache_data
def _catalog() -> list[str]:
    if not DATA_DIR.exists():
        return []
    return sorted(p.name for p in DATA_DIR.glob("*.csv"))


def available_files(topic_slug: str) -> list[str]:
    """All processed CSV filenames whose name starts with `{topic_slug}__`."""
    prefix = f"{topic_slug}__"
    return [f for f in _catalog() if f.startswith(prefix)]


def find_file(topic_slug: str, contains: str = "") -> str | None:
    """Best-effort match: prefix on topic_slug, substring on `contains`."""
    candidates = available_files(topic_slug)
    if contains:
        matched = [f for f in candidates if contains.lower() in f.lower()]
        if matched:
            candidates = matched
    return candidates[0] if candidates else None


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    df = pd.read_csv(path)
    if "year" in df.columns:
        # ESS round 10 spanned 2021-2022; individual parser scripts pull this label
        # verbatim from the workbook, so it comes through as either "2021/22" or
        # "2021/2022" depending on which sheet it was read from. Normalize here so
        # every chart's x-axis is consistent regardless of which ETL script ran.
        df["year"] = df["year"].astype(str).str.replace("2021/2022", "2021/22", regex=False)
    return df


def load(topic_slug: str, contains: str = "") -> pd.DataFrame | None:
    """Convenience: find + load in one call. Returns None if nothing matches."""
    fname = find_file(topic_slug, contains)
    if fname is None:
        return None
    return load_csv(fname)


def load_all(topic_slug: str) -> dict[str, pd.DataFrame]:
    """All processed tables for a topic, keyed by filename."""
    return {f: load_csv(f) for f in available_files(topic_slug)}
