#!/usr/bin/env python3
"""
This module contains index_range function used to determine start & end
index for a list of items when paginating.
"""
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end index for pagination based on page number
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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = 'Popular_Baby_Names.csv'

    def __init__(self):
        """This is the initializing function
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """This function returns content of page
        """
        # return list(index_range(page, page_size))
        assert isinstance(
            page, int) and page > 0, "must be a positive integer"
        assert isinstance(
            page_size, int) and page_size > 0, "must be a positive integer"

        # Use the index_range function to calculate start and end indexes
        start, end = index_range(page, page_size)

        # Get the dataset
        dataset = self.dataset()

        # Return the appropriate slice of the dataset or an empty list if out
        # of range
        if start >= len(dataset):
            return []

        return dataset[start:end]
