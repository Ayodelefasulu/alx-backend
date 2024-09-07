#!/usr/bin/env python3
"""
This module contains index_range function used to determine the start and end
index for a list of items when paginating.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end index for pagination based on the page number
    and the size of each page.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index (inclusive) and
        the end index (exclusive) for the requested page.
    """
    start: int = (page - 1) * page_size
    end: int = start + page_size
    return (start, end)
