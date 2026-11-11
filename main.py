from crawler import WebsiteCrawler
from chunker import TextChunker
from vector_store import VectorStore
from agent import ResearchAgent
from web_search import WebSearch


def main():

    print("\n==============================")
    print("AI Research Agent")
    print("==============================\n")

    url = input("Enter Website URL: ")

    print("\n[1] Crawling Website...")

    crawler = WebsiteCrawler()

    content = crawler.crawl_website(
        url,
        max_pages=10
    )

    print("\nTotal Combined Content Length:")

    print(len(content))

    print("[✓] Website Scraped")

    print("\n[2] Creating Chunks...")

    chunker = TextChunker()

    chunks = chunker.chunk_text(
        content,
        chunk_size=1000
    )

    print(
        f"[✓] Total Chunks Created: {len(chunks)}"
    )

    print("\n[3] Building Vector Database...")

    vector_store = VectorStore()

    vector_store.build_index(
        chunks
    )

    print("[✓] Vector Index Ready")

    print("\n[4] Initializing Research Agent...")

    agent = ResearchAgent()

    web_search = WebSearch()

    print("[✓] Agent Ready")

    print("\n===================================")
    print("Ask Questions About The Website")
    print("Type 'exit' to quit")
    print("===================================\n")

    while True:

        question = input(
            "Ask Question: "
        )

        if question.lower() == "exit":
            break

        # ======================================
        # Research Report Mode
        # ======================================

        if question.lower().startswith(
            "research "
        ):

            topic = question.replace(
                "research ",
                ""
            )

            relevant_chunks = (
                vector_store.search(
                    topic,
                    top_k=20
                )
            )

            report = (
                agent.generate_report(
                    topic,
                    relevant_chunks
                )
            )

            print("\nREPORT:\n")

            print(report)

            print(
                "\n" + "=" * 60 + "\n"
            )

            continue

        # ======================================
        # Website Search
        # ======================================

        relevant_chunks = (
            vector_store.search(
                question,
                top_k=10
            )
        )

        answer = (
            agent.answer_question(
                question,
                relevant_chunks
            )
        )

        # ======================================
        # Web Search Fallback
        # ======================================

        if answer.strip().lower().startswith(
            "information not found"
        ):

            print(
                "\n[INFO] Website doesn't contain answer."
            )

            print(
                "[INFO] Searching the Web...\n"
            )

            results = (
                web_search.search(
                    question,
                    max_results=5
                )
            )

            print(
                f"\nTOTAL RESULTS FOUND: {len(results)}"
            )

            if len(results) > 0:

                answer = (
                    agent.answer_from_web(
                        question,
                        results
                    )
                )

            else:

                answer = (
                    "No web search results found."
                )

        # ======================================
        # Print Final Answer
        # ======================================

        print("\nAnswer:\n")

        print(answer)

        print(
            "\n" + "=" * 60 + "\n"
        )


if __name__ == "__main__":
    main()