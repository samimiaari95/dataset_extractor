from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def iter_merra_nc4_urls(
    base_url: str,
    *,
    start_year: int = 1980,
    end_year: int = 2021,
    start_month: int = 1,
    end_month: int = 12,
):
    """Collect downloadable .nc4 links from an MERRA2 directory index."""
    session = requests.Session()

    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            month_label = str(month).zfill(2)
            page_url = f"{base_url.rstrip('/')}/{year}/{month_label}/"
            response = session.get(page_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "xml" not in href.lower() and href.lower().endswith(".nc4"):
                    yield urljoin(page_url, href)


def save_merra_urls(
    output_path: str | Path,
    base_url: str,
    *,
    start_year: int = 1980,
    end_year: int = 2021,
    start_month: int = 1,
    end_month: int = 12,
) -> list[str]:
    """Write discovered MERRA URLs to a text file and return them."""
    links = list(
        iter_merra_nc4_urls(
            base_url,
            start_year=start_year,
            end_year=end_year,
            start_month=start_month,
            end_month=end_month,
        )
    )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(links) + ("\n" if links else ""), encoding="utf-8")
    return links
