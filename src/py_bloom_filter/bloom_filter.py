from collections.abc import Hashable

from typing_extensions import override

from py_bloom_filter.bit_vector import BitVector


class BloomFilter:
    """
    A simple Bloom Filter implementation using a BitVector to support
    probabilistic set membership testing.

    A Bloom filter can quickly test whether an element is possibly in a set or definitely not in it.

    - If `bloom_filter.contains(x)` returns `False`, then `x` is definitely not in the set.
    - If it returns `True`, `x` may be in the set (with some false positive probability).
    """

    def __init__(self, num_bits: int, num_hashes: int):
        """
        Initializes a Bloom Filter with a given bit vector size and number of hash functions.

        Args:
            num_bits (int): The size of the bit vector (number of bits).
            num_hashes (int): The number of hash functions to use.

        Raises:
            ValueError: If `num_bits` or `num_hashes` is < 0.
        """
        if num_bits < 0:
            raise ValueError("expected num_bits to be >= 0")
        if num_hashes < 0:
            raise ValueError("expected num_hashes to be >= 0")
        self._size: int = num_bits
        self._bit_vector: BitVector = BitVector(num_bits)
        self._num_hashes: int = num_hashes

    def size(self) -> int:
        """
        Returns the `size` of the BitVector
        """
        return self._size

    def num_hashes(self) -> int:
        """
        Returns the number of hash functions used.
        """
        return self._num_hashes

    def _get_hashes(self, elem: Hashable) -> list[int]:
        """
        Generates `num_hash` hashes for the given element.

        Args:
            elem (Hashable): The element to hash.

        Returns:
            list[int]: A list of `num_hash` integer hash values.
        """
        # provides an initial hash to start with
        base_hash = hash(elem)

        hashes: list[int] = []
        for i in range(self._num_hashes):
            # re-hash the hash with a salt (in this case index)
            combined_hash = hash((base_hash, i))

            hashes.append(combined_hash)
        return hashes

    def insert(self, elem: Hashable):
        """
        Inserts an element into the Bloom filter.

        Args:
            elem (Hashable): The element to insert.
        """
        hashes: list[int] = self._get_hashes(elem)

        for hash in hashes:
            self._bit_vector.set(hash % self._size, True)

    def contains(self, elem: Hashable) -> bool:
        """
        Tests whether an element is possibly in the Bloom filter.

        Args:
            elem (Hashable): The element to check.

        Returns:
            If `bloom_filter.contains(x)` returns `False`, then `x` is definitely not in the set.
            If it returns `True`, `x` may be in the set (with some false positive probability).
        """
        hashes: list[int] = self._get_hashes(elem)

        for hash in hashes:
            if not self._bit_vector.get(hash % self._size):
                return False

        return True

    @override
    def __repr__(self) -> str:
        return f"BloomFilter(size={self._size}, BitVector={self._bit_vector!r}, num_hashes={self._num_hashes})"
