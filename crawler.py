import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class WebsiteCrawler:

    def __init__(self):

        self.visited = set()

    def scrape_page(self, url):

        try:

            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=20
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup(
                [
                    "script",
                    "style",
                    "noscript",
                    "iframe"
                ]
            ):
                tag.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            return text, soup

        except Exception as e:

            print(f"Error crawling {url}")

            print(e)

            return "", None

    def extract_internal_links(
        self,
        url,
        soup
    ):

        links = []

        base_domain = urlparse(
            url
        ).netloc

        for tag in soup.find_all(
            "a",
            href=True
        ):

            href = tag["href"]

            full_url = urljoin(
                url,
                href
            )

            parsed = urlparse(
                full_url
            )

            if parsed.netloc == base_domain:

                if full_url not in links:

                    links.append(
                        full_url
                    )

        return links

    def crawl_website(
        self,
        url,
        max_pages=10
    ):

        all_content = []

        text, soup = self.scrape_page(
            url
        )

        if text:

            all_content.append(
                text
            )

        if soup is None:

            return ""

        links = self.extract_internal_links(
            url,
            soup
        )

        print(
            f"\nFound {len(links)} internal links"
        )

        count = 0

        for link in links:

            if count >= max_pages:
                break

            if link in self.visited:
                continue

            print(
                f"Crawling: {link}"
            )

            self.visited.add(
                link
            )

            page_text, _ = (
                self.scrape_page(
                    link
                )
            )

            if page_text:

                all_content.append(
                    page_text
                )

            count += 1

        return "\n".join(
            all_content
        )