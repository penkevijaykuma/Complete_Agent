from ddgs import DDGS


class WebSearch:

    def search(self, query, max_results=5):

        search_queries = [
    query,
    query.replace("interview", "").strip(),
    query.replace("latest", "").strip()
]

        for search_query in search_queries:

            try:

                print(f"\nTrying Query: {search_query}")

                with DDGS() as ddgs:

                    results = list(
                        ddgs.text(
                            search_query,
                            max_results=max_results
                        )
                    )

                    if results:

                        print(
                            f"Found {len(results)} results"
                        )

                        return [
                            {
                                "title": r.get(
                                    "title", ""
                                ),
                                "body": r.get(
                                    "body", ""
                                ),
                                "href": r.get(
                                    "href", ""
                                ),
                            }
                            for r in results
                        ]

            except Exception as e:

                print(
                    f"Failed Query: {search_query}"
                )

                print(e)

        return []