import streamlit as st


def insight(text: str, *, source: str = "Irish Social Attitudes: 2023 report") -> None:
    """A consistent 'what this means' callout under a chart."""
    st.info(f"**Insight.** {text}\n\n*Source: {source}*")


def data_insight(text: str) -> None:
    """Insight derived from the data directly (topic not covered in the source report)."""
    st.info(f"**Insight.** {text}\n\n*Derived from ESS Round 11 Ireland data (not covered in the published report).*")


def page_header(title: str, subtitle: str = "") -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()
