import json
from json import JSONDecodeError
# from pprint import pprint as pp
from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """
    Менеджер постов - загружает, ищет, вытаскивает по pk и пользователю.
    """
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """
        Загружает данные из JSON файла и возвращает список словарей.
        :return: список словарей с постами.
        """

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удаётся получить данные из файла {self.path}')
        return posts_data

    def _load_posts(self):
        """
        Получает все посты.
        :return: список экземпляров класса Post.
        """

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data] # это эквивалент Post(poster_name=posts_data['poster_name'], poster_avatar=posts_data['poster_avatar'], и т.д.)
        return list_of_posts

    def get_all(self):
        """
        Получает все посты.
        :return: список экземпляров класса Post.
        """

        posts = self._load_posts()
        return posts

    def get_by_pk(self, pk):
        """
        Получает пост по PK.
        :return: искомый экземпляр класса Post/
        """

        if type(pk) != int:
            raise TypeError("pk должно быть цэлым числом.")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """
        Ищет посты, где в контенте всречается substring.
        :return: список экземпляров класса Post, содержащих искомое в post.content.
        """

        if type(substring) != str:
            raise TypeError("substring должно быть строкой.")

        substring = substring.lower()
        posts = self._load_posts()
        matching_posts = [post for post in posts if substring in post.content.lower()]
        # matching_posts = [] # однострочник - аналог этой записи.
        # for post in posts:
        #     if substring in post.content.lower():
        #         matching_posts.append(post)
        return matching_posts

    def search_by_poster(self, user_name):
        """
        Ищет посты по автору.
        :return: список экземпляров класса Post, содержащих искомое в post.poster_name.
        """

        if type(user_name) != str:
            raise TypeError("user_name должно быть строкой.")

        user_name = user_name.lower()
        posts = self._load_posts()
        matching_posts = [post for post in posts if user_name == post.poster_name.lower()]

        return matching_posts


# pd = PostDAO('../../data/posts.json')
# pp(pd._load_posts())
