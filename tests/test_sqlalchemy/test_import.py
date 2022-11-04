from ._base import PostFilter


def test_subclass_init() -> None:
    assert PostFilter.__filter_spec__ == [
        PostFilter.id,
        PostFilter.title,
        PostFilter.user_username,
    ]
