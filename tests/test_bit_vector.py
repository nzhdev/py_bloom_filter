import pytest

from py_bloom_filter import BitVector


@pytest.fixture
def bv():
    return BitVector(8)


def test_bitvector_initialization_size():
    assert BitVector(0).size() == 0
    assert BitVector(17).size() == 17
    assert BitVector(24).size() == 24


def test_bitvector_negative_initialization_raises():
    with pytest.raises(ValueError):
        _ = BitVector(-1)


def test_set_and_get_bit_true(bv: BitVector):
    bv.set(3, True)
    assert bv.get(3) is True


def test_set_and_get_bit_false(bv: BitVector):
    bv.set(3, True)
    bv.set(3, False)
    assert bv.get(3) is False


def test_get_out_of_bounds_raises(bv: BitVector):
    with pytest.raises(ValueError):
        _ = bv.get(8)


def test_set_out_of_bounds_raises(bv: BitVector):
    with pytest.raises(ValueError):
        bv.set(10, True)


def test_repr_contains_bit_vector(bv: BitVector):
    assert "BitVector" in repr(bv)
