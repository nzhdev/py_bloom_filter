class BitVector:
    """
    Fixed-size array of bits backed by a bytearray for efficient storage.

    Supports setting and reading individual bits in the array.
    """

    def __init__(self, num_bits: int):
        """
        Initializes BitVector with `num_bits` bits.

        Args:
            num_bits (int): the number of bits we wish to store in BitVector.

        Raises:
            ValueError: when `num_bits` is not >= 0.
        """

        if num_bits < 0:
            raise ValueError(f"expected `num_bits` to be >= 0, got: {num_bits}")
        self._size = num_bits
        self._inner = bytearray((num_bits + 7) // 8)

    def size(self) -> int:
        """
        Returns the `size` of the BitVector
        """
        return self._size

    def get(self, index: int) -> bool:
        """
        Retrieves the boolean value of the bit at the specified `index`.

        Args:
            index (int): The bit index to access. Must be in [0, `size`).

        Returns:
            bool: True if the bit at the given index is set to True, False otherwise.

        Raises:
            ValueError: If `index` is out of bounds (not in range [0, `size`)).
        """

        if index < 0 or index >= self._size:
            raise ValueError(
                f"expected `index` to be between [0, {self.size()}), got: {index}"
            )

        byte_index = index // 8
        bit_offset = index % 8

        return (self._inner[byte_index] >> bit_offset) & 1 == 1

    def set(self, index: int, value: bool):
        """
        Sets the boolean value of the bit at the specified `index` to equal `value`.

        Args:
            index (int): The bit `index` to access. Must be between 0 and `size - 1`.

        Raises:
            ValueError: If `index` is out of bounds (not in range [0, `size`)).
        """
        if index < 0 or index >= self.size():
            raise ValueError(
                f"expected `index` to be between 0 and {self.size()}, got: {index}"
            )
        byte_index = index // 8
        bit_offset = index % 8

        if value:
            self._inner[byte_index] |= 1 << bit_offset
        else:
            self._inner[byte_index] &= ~(1 << bit_offset)

    def __repr__(self) -> str:
        return f"BitVector(size={self._size}, bytearray={self._inner})"
