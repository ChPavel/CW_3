import json
from json import JSONDecodeError
from exceptions.data_exceptions import DataSourceError
from bp_posts.dao.comment import Comment

class CommentsDAO:

    """
    Менеджер комментариев
    """
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """
        Загружает данные из JSON файла.
        :return: список словарей.
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                comments_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удаётся получить данные из файла {self.path}')
        return comments_data

    def _load_comments(self):
        """
        Получает все комменты.
        :return: список экземпляров класса Сomment.
        """
        comments_data = self._load_data()
        list_of_comments = [Comment(**comment_data) for comment_data in comments_data]
        return list_of_comments

    def get_all(self):
        comments = self._load_comments()
        return comments

    def get_comments_by_post_pk(self, post_pk: int):
        """
        Получает все комментарии к определённому посту по его pk
        :return: список экземпляров класса Сomment.
        """
        comments = self._load_comments()
        comments_match = [c for c in comments if c.post_id == post_pk]
        return comments_match



# cd = CommentsDAO("../tests/comments_mock.json")
# print(cd.get_comments_by_post_pk(2))

