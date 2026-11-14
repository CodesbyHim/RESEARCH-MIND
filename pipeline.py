from collections.abc import Callable
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def _content_to_text(content) -> str:
    """Convert LangChain message content into plain text.

    Gemini and other chat models may return message content as a list of
    text/content blocks instead of one string.
    """
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                # Common LangChain multimodal/text block formats.
                text_value = item.get("text")
                if text_value is not None:
                    parts.append(str(text_value))
                elif item.get("content") is not None:
                    parts.append(str(item["content"]))
            else:
                parts.append(str(item))
        return "\\n".join(part for part in parts if part).strip()

    if isinstance(content, dict):
        text_value = content.get("text")
        if text_value is not None:
            return str(text_value).strip()

    return str(content).strip()


def _require_text(value, stage_name: str) -> str:
    """Normalize a stage result and raise a clear error if it is empty."""
    text = _content_to_text(value)
    if not text:
        raise RuntimeError(f"The {stage_name} returned no content.")
    return text


def run_research_pipeline(
    topic: str,
    progress_callback: Callable[[str, str], None] | None = None,
) -> dict:
    """Run the four research stages and optionally report stage status.

    progress_callback receives (stage_name, status), where status is
    "running" or "done". The Streamlit UI uses this to update its progress cards.
    """
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Research topic must be a non-empty string.")

    topic = topic.strip()
    state = {}

    def notify(stage: str, status: str) -> None:
        if progress_callback is not None:
            progress_callback(stage, status)

    # Step 1: Search
    notify("search", "running")
    print("\\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = _require_text(
        search_result["messages"][-1].content,
        "Search Agent",
    )
    notify("search", "done")
    print("\\n search result ", state["search_results"])

    # Step 2: Reader
    notify("reader", "running")
    print("\\n" + " =" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            "identify the most relevant URL and use the scraping tool to read it. "
            "Use a URL exactly as provided in the search results.\\n\\n"
            f"Search Results:\\n{state['search_results']}"
        )]
    })
    state["scraped_content"] = _require_text(
        reader_result["messages"][-1].content,
        "Reader Agent",
    )
    notify("reader", "done")
    print("\\nscraped content: \\n", state["scraped_content"])

    # Step 3: Writer
    notify("writer", "running")
    print("\\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\\n{state['search_results']}\\n\\n"
        f"DETAILED SCRAPED CONTENT:\\n{state['scraped_content']}"
    )
    writer_result = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    state["report"] = _require_text(writer_result, "Writer Chain")
    notify("writer", "done")
    print("\\n Final Report\\n", state["report"])

    # Step 4: Critic
    notify("critic", "running")
    print("\\n" + " =" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    critic_result = critic_chain.invoke({"report": state["report"]})
    state["feedback"] = _require_text(critic_result, "Critic Chain")
    notify("critic", "done")
    print("\\n critic report \\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\\n Enter a research topic : ")
    run_research_pipeline(topic)
