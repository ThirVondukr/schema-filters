from sqlalchemy import select

from ._base import Post, PostFilter, User

Schema = PostFilter.schema()


def test_apply_filter() -> None:
    stmt = select(Post).join(User, User.id == Post.user_id)
    filtered = PostFilter.apply(
        stmt,
        Schema(
            id__eq=42,
            id__not_eq=69,
            title__eq="Post Title",
            user_username__eq="Username",
        ),
    )
    expected = stmt.where(
        Post.id == 42,
        Post.id != 69,
        Post.title == "Post Title",
        User.username == "Username",
    )
    assert filtered.compare(expected)
