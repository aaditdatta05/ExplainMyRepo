import os

import httpx
import streamlit as st

DEFAULT_API_BASE_URL = os.getenv("EXPLAIN_MY_REPO_API_BASE_URL", "http://127.0.0.1:8000")


def _render_analysis(payload: dict[str, object]) -> None:
    st.subheader("Overview")
    st.write(payload.get("overview", "No overview available."))

    st.subheader("Modules")
    st.write(payload.get("modules", "No module summary available."))

    st.subheader("Flow")
    st.write(payload.get("flow", "No workflow summary available."))

    citations = payload.get("citations", [])
    if isinstance(citations, list) and citations:
        st.subheader("Citations")
        st.table(citations)

    with st.expander("Markdown Output"):
        markdown_output = payload.get("markdown", "")
        if isinstance(markdown_output, str):
            st.markdown(markdown_output)

    with st.expander("Raw JSON"):
        st.json(payload)


def main() -> None:
    st.set_page_config(page_title="ExplainMyRepo", page_icon="🧠", layout="centered")
    st.title("ExplainMyRepo")
    st.caption("Simple UI for repository explanation input and output")

    api_base_url = st.text_input("API Base URL", value=DEFAULT_API_BASE_URL)
    repository_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repo",
    )

    if st.button("Analyze", type="primary"):
        if not repository_url.strip():
            st.warning("Please enter a repository URL.")
            return

        endpoint = f"{api_base_url.rstrip('/')}/analyze"
        with st.spinner("Analyzing repository..."):
            try:
                response = httpx.post(
                    endpoint,
                    json={"repository_url": repository_url.strip()},
                    timeout=60.0,
                )
            except httpx.HTTPError as exc:
                st.error(f"Request failed: {exc}")
                return

        if response.status_code != 200:
            try:
                error_payload = response.json()
            except ValueError:
                error_payload = {"message": response.text}

            message = error_payload.get("message") or error_payload.get("detail") or response.text
            st.error(f"API error ({response.status_code}): {message}")
            return

        _render_analysis(response.json())


if __name__ == "__main__":
    main()
