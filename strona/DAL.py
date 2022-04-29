from .models import Tags, Post

class Database:
    def add_tag(self, tag_name):
        t = Tags(tagi=tag_name)
        t.save()

    def retrieve_tag(self, tag_id):
        retrival = Tags.objects.all()
        return retrival[tag_id]

    def modify_tag_name_by_id(self, tag_id, name):
        g_x = Tags.objects.get(id=tag_id)
        g_x.tagi = name
        g_x.save()
#do poprawienia
    def retrieve_posts_by_date(self, date):
        retrive = Post.objects.all().filter(date_created=date)
        return retrive

    def retrieve_post_by_title(self, tittle):
        retri = Post.objects.all().filter(title=tittle)
        return retri

    def modify_post_content_by_title(self, tittle, content):
        new_con = Post.objects.all().filter(title=tittle)
        new_con = content
        new_con.save()

    def add_new_post(self):
        pass
