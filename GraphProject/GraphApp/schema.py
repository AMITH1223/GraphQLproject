import graphene
from graphene_django.types import DjangoObjectType
from .models import Post, Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.DateTime()
        author = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, title, description, publish_date, author):
        post = Post(title=title, description=description, publish_date=publish_date, author=author)
        post.save()
        return CreatePost(post=post)

class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        author = graphene.String()
        post_id = graphene.Int()  

    comment = graphene.Field(CommentType)

    def mutate(self, info, text, author, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        comment = Comment(text=text, author=author, post=post)
        comment.save()
        return CreateComment(comment=comment)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.DateTime()
        author = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title, description, publish_date, author):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        post.title = title
        post.description = description
        post.publish_date = publish_date
        post.author = author
        post.save()

        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            success = True
        except Post.DoesNotExist:
            success = False

        return DeletePost(success=success)
    

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            post = Comment.objects.get(pk=id)
            post.delete()
            success = True
        except Post.DoesNotExist:
            success = False

        return DeleteComment(success=success)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    delete_comment = DeleteComment.Field() 

schema = graphene.Schema(query=Query, mutation=Mutation)
