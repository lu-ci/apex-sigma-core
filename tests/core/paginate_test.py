import pytest

from sigma.core.utilities.paginate import paginate


class TestPaginate(object):
    # List cannot be None but can be empty
    def test_page(self):
        assert paginate([], 0) == ([], 1)
        assert paginate([], 1) == ([], 1)
        assert paginate([], 2) == ([], 1)
        assert paginate([], "0") == ([], 1)
        assert paginate([], "1") == ([], 1)
        assert paginate([], "2") == ([], 1)
        assert paginate([], None) == ([], 1)

    # Span cannot be None or 0
    def test_page_size(self):
        nums = list(range(1, 15))
        assert paginate(nums, 1) == (nums[0:10], 1)
        assert paginate(nums, 3) == (nums[10:20], 2)
        assert paginate(nums, 3, span=5) == (nums[10:15], 3)
