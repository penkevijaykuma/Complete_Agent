from ddgs import DDGS

with DDGS() as ddgs:

    results = list(
        ddgs.text(
            "MS Dhoni",
            max_results=5
        )
    )

    print(results)