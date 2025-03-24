from django.contrib import admin

from posts.models import Group, Post, Comment, Follow


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Group, GroupAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group')
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date', 'author', 'group')
    ordering = ('-pub_date',)


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    search_fields = ('author__username', 'post__text')
    list_filter = ('created', 'post')


admin.site.register(Comment, CommentAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')
    list_filter = ('user', 'following')


admin.site.register(Follow, FollowAdmin)
