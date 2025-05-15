# py-bloom-filter

A simple **Bloom Filter** implementation in Python.

This is mostly a short project to get used to uv tooling.

# API Reference

- BloomFilter(num_bits: int, num_hashes: int): Create a new filter.
- insert(elem: Hashable): Add an element to the filter.
- contains(elem: Hashable) -> bool: Check if an element _might_ be in the filter.
- size() -> int: Get the number of bits the filter can store.
- num_hashes() -> int: Get the number of hash functions.
