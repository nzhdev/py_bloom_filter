import pytest
from py_bloom_filter import BloomFilter


@pytest.fixture
def bf():
    return BloomFilter(100, 5)


def test_insert_and_contains(bf):
    items = ["foo", "bar", 42, (1, 2)]
    for item in items:
        bf.insert(item)

    for item in items:
        assert bf.contains(item), f"{item!r} should be in the filter"


def test_not_inserted_items():
    """
    Flaky test: occasionally fails due to excess Bloom filter false positives
    Expected false positive rate is 1/11 => 18 expected false positives
    https://hur.st/bloomfilter/?n=100&p=&m=1024&k=1
    """
    bf = BloomFilter(1024, 1)

    for i in filter(lambda x: x % 3 == 0, range(0, 300)):
        elem = hash(i)
        bf.insert(elem)

    for i in filter(lambda x: x % 3 == 0, range(0, 300)):
        elem = hash(i)
        assert bf.contains(elem), f"{elem!r} should be in the filter"

    false_positive = 0

    for i in range(1200, 1400):
        elem = hash(i)
        if bf.contains(elem):
            false_positive += 1

    assert false_positive <= 30, (
        f"expected <= 30 false positives, got: {false_positive}"
    )


def test_insert_duplicates(bf):
    bf.insert("repeat")
    bf.insert("repeat")
    assert bf.contains("repeat")


def test_empty_filter():
    bf = BloomFilter(100, 5)
    assert not bf.contains("anything"), "Empty filter should not contain any element"


@pytest.mark.parametrize("num_bits, num_hashes", [(-1, 3), (10, -5)])
def test_invalid_sizes(num_bits, num_hashes):
    with pytest.raises(ValueError):
        BloomFilter(num_bits, num_hashes)


def test_bit_vector_size():
    size = 128
    bf = BloomFilter(size, 3)
    assert bf.size() == size


def test_num_hashes():
    size = 128
    bf = BloomFilter(size, 9)
    assert bf.num_hashes() == 9


def test_repr_contains_bloom_filter(bf):
    assert "BloomFilter" in repr(bf), f"got: {repr(bf)}"


def test_repr_contains_bit_vector(bf):
    assert "BitVector" in repr(bf), f"got: {repr(bf)}"
