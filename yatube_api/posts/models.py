from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import TEXT_RESTRICTION

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок')
    slug = models.SlugField(unique=True,
                            verbose_name='Уникальный идентификатор')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title[:TEXT_RESTRICTION]


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    image = models.ImageField(upload_to='posts/',
                              null=True, blank=True,
                              verbose_name='Изображение')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              verbose_name='Группа')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:TEXT_RESTRICTION]


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')
    text = models.TextField(verbose_name='Текст комментария')
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


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriptions',
                             verbose_name='Подписчик')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='followers',
                                  verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='check_not_self_follow',
            ),
        )

    def __str__(self):
        return (f'Пользователь {self.user.username}'
                f'подписан на: {self.following}')
