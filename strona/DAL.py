from .models import Tags, Post, Multimedia


class Database:
    def add_tag(self, tag_name):
        t = Tags(tagi=tag_name)
        t.save()

    def retrieve_tag(self, tag_id):
        retrival = Tags.objects.all().values()
        return retrival[tag_id]

    def modify_tag_name_by_id(self, tag_id, name):
        g_x = Tags.objects.get(id=tag_id)
        g_x.tagi = name
        g_x.save()

    def retrieve_post_by_title(self, tittle):
        retri = Post.objects.filter(title=tittle).values()
        return retri

    def modify_post_content_by_title(self, tittle, content):
        new_con = Post.objects.filter(title=tittle)
        new_con.content = content
        new_con.save()

    def modify_post_by_id(self,id, tittle, content, author):
        new_con = Post.objects.get(id=id)
        new_con.title = tittle
        new_con.content = content
        new_con.author = author
        new_con.save()

    def add_new_post(self, title, content, author):
        new_post = Post(title=title, content=content, author=author)
        new_post.save()

    def change_tags_in_post(self, tag_s, post_id):
        retri = Post.objects.get(id=post_id)
        new_tags = Tags.objects.create(tagi=tag_s)
        retri.tag.add(new_tags)
        retri.save()

    def pulish_post(self, id, choice):
        if choice is True:
            pub_post = Post.objects.get(id=id)
            pub_post.publish = choice
            pub_post.save()
        elif choice is False:
            pub_post = Post.objects.get(id=id)
            pub_post.publish = choice
            pub_post.save()
        else:
            raise ValueError("Choice must be boolean, True to publish or False to unpublish")


    def retrive_posts_values(self):
        retri = Post.objects.all().values().order_by("id")
        retri2 = Post.objects.all()[0].tag.all()
        all_data = (retri, retri2)
        return all_data

    def delete_post_by_id(self, id):
        instance = Post.objects.get(id=id)
        instance.delete()

    def delete_multimedia_by_id(self, id):
        retri = Multimedia.objects.get(id=id)
        retri.delete()


    def retrive_mutlimedia(self):
        retri = Multimedia.objects.all()
        return retri.photos.url

