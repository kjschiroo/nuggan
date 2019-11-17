"""Tests for nuggan.id_maker"""
import pytest

from nuggan import id_maker


def test_created_ids_are_valid():
    """Should be able to create an id and have the id be valid."""
    identifier = id_maker.create_id('foobar')

    assert id_maker.is_valid_id(identifier)


def test_arbitrary_id_is_not_valid():
    """If given an arbitrary id matching the format it should not be valid."""
    some_id = 'foobar-5bf849aa-5555-4444-3333-6382850e4b44-222222222222'

    assert not id_maker.is_valid_id(some_id)


def test_salt_changes_hash_value():
    """If given a salt, it should be incorporated into the id checksum."""
    salt = 'random-salt'
    identifier = id_maker.create_id('foobar', salt=salt)
    prefixed = id_maker.parse_id(identifier)['prefixed_id']

    assert identifier == id_maker._append_hash(prefixed, salt=salt)
    assert identifier != id_maker._append_hash(prefixed)


def test_id_maker_created_validates():
    """If an id maker creates an id, then it should also validate the id."""
    maker = id_maker.IdMaker('some-salt')

    identifier = maker.create_id('prefix')

    assert maker.is_valid_id(identifier)


def test_prefixes_dont_allow_dash():
    """If given a prefix with a dash an error should be raised."""
    with pytest.raises(ValueError):
        id_maker.create_id('no-dashes-allowed')


def test_non_nuggan_id_is_not_valid():
    """
    If given an id that doesn't match our expected format at all it should
    be considered not a valid id.
    """
    assert not id_maker.is_valid_id('this_is_in_no_way_valid')
