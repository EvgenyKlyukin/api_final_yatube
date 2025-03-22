from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import TEXT_RESTRICTION

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    image = models.ImageField(upload_to='posts/',
                              null=True,
                              blank=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:TEXT_RESTRICTION]


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления',
                                   auto_now_add=True,
                                   db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return (f'Комментарий от {self.author.username} '
                f'к посту "{self.post}"')


class Group(models.Model):
    title = models.CharField(max_length=200,
                             related_name='groups')
    slug = models.SlugField(unique=True,
                            related_name='groups')
    description = models.TextField()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title[:TEXT_RESTRICTION]


class Follow(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='follows')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='follows')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Пользователь {self.user.username}'
                f'подписан на: {self.following}')
