import pytest as pytest
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO


def check_fields(post):

    filds = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    for field in filds:
        assert hasattr(post, field), f"Нет поля {field}"

    # Вместо нижеследующих строк используем цыкл.
    ## функция hasattr(объект, поле) проверяет есть ли поле у объекта.
    # assert hasattr(post, "poster_name"), "Нет поля"
    # assert hasattr(post, "poster_avatar"), "Нет поля"
    # assert hasattr(post, "pic"), "Нет поля"
    # assert hasattr(post, "content"), "Нет поля"
    # assert hasattr(post, "views_count"), "Нет поля"
    # assert hasattr(post, "likes_count"), "Нет поля"
    # assert hasattr(post, "pk"), "Нет поля"


class TestPostDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("post_mock.json")
        return post_dao_instance

    ### Функция получения всех постов.

    def test_get_all_types(self, post_dao):

        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result. " \
                                    "(Неверный тип результата. " \
                                    "Пооверка - возвращается список или нет.)"

        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item. " \
                                    "(Неправильный тип для одного элемента результата. " \
                                    "Пооверка - возвращается первый элемент класс Post или нет.)"

    def test_get_all_fields(self, post_dao):
        posts = post_dao.get_all()
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_all_correct_ids(self, post_dao):
        posts = post_dao.get_all()

        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts ])
        assert pks == correct_pks, "Не совпадают полученные id."

    ### Функция получения одного по pk.

    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "Incorrect type for result single item."

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(999)
        assert post is None, "Shoult be None for not existent pk"


    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Incorrect post.pk for requesten post with pk = {pk}"

    ### Функция получения одного по вхождению строки.

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("ага")
        assert type(posts) == list, "Incorrect type for result."
        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item."

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_in_content("ага")
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("9999099999")
        assert posts == [], "Shoult be [] for not substring not found"

    @pytest.mark.parametrize("s, expected_pks", [
        ("Ага", {1}),
        ("Вышел", {2}),
        ("на", {1, 2, 3})
    ])
    def test_search_in_content_results(self, post_dao, s, expected_pks):
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incorrect result searching for {s}."

    ### Функция получения одного по имени автора.

    def test_search_by_poster_types(self, post_dao):
        posts = post_dao.search_by_poster("leo")
        assert type(posts) == list, "Incorrect type for result."
        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item."

    def test_search_by_poster_fields(self, post_dao):
        posts = post_dao.search_by_poster("leo")
        post = posts[0]
        check_fields(post)

    def test_search_by_poster_not_found(self, post_dao):
        posts = post_dao.search_by_poster("9999099999")
        assert posts == [], "Shoult be [] for not poster_name not found"

    @pytest.mark.parametrize("s, expected_pks", [
        ("leo", {1}),
        ("johnny", {2}),
        ("hank", {3})
    ])
    def test_search_by_poster_results(self, post_dao, s, expected_pks):
        posts = post_dao.search_by_poster(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incorrect result searching for {s}."