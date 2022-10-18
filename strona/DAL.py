from .models import Tags, Post, Multimedia, Comment, Galery, Registration


class Database:
    #tagi
    def add_tag(self, tag_name):
        t = Tags(tagi=tag_name)
        t.save()

    def retrieve_tag(self, tag_id, do_all):
        if do_all is True:
            retri = Tags.objects.all().values()
            return retri
        elif do_all is False:
            retrival = Tags.objects.get(id=tag_id)
            return retrival
        else:
            raise ValueError("Choice must be boolean, True to retrive all tags or False to retrive one by id")

    def modify_tag_name_by_id(self, tag_id, name):
        g_x = Tags.objects.get(id=tag_id)
        g_x.tagi = name
        g_x.save()

    #posty
    def retrieve_post_by_title(self, tittle):
        retri = Post.objects.filter(title=tittle).values()
        return retri

    def retrieve_post_by_id(self, id):
        retri = Post.objects.filter(id=id).values()
        return retri

    def retrive_posts_values(self):
        retri = Post.objects.all().values().order_by("id")
        retri2 = Post.objects.all()[0].tag.all()
        all_data = (retri, retri2)
        return all_data


    def modify_post_content_by_title(self, tittle, content):
        new_con = Post.objects.filter(title=tittle)
        new_con.content = content
        new_con.save()

    def modify_post_by_id(self,id , tittle, content, author):
        new_con = Post.objects.get(id=id)
        new_con.title = tittle
        new_con.content = content
        new_con.author = author
        new_con.save()

    def do_exi(self, tag):
        fetch_tags = Tags.objects.all()
        list_of_tags = list(str(item.tagi) for item in fetch_tags)
        if str(tag) in list_of_tags:
            return 1
        if str(tag) not in list_of_tags:
            return 0

    def add_new_post(self, title, content, author, choice, tagi_name, event):
        # jak tag istnieje to zamiast dodac nowy pobiera z bazy
        def do_exist_tag(tag):
            fetch_tags = Tags.objects.all()
            list_of_tags = list(str(item.tagi) for item in fetch_tags)
            if str(tag) in list_of_tags:
                return 1
            if str(tag) not in list_of_tags:
                return 0

        tagi_name = tagi_name.split(",")
        if choice == True:
            new_post = Post(title=title, content=content, author=author, publish=choice, event=event)
            new_post.save()
            for item in range(len(tagi_name)):
                #print(do_exist_tag(item))
                if do_exist_tag(tagi_name[item]) == 1:
                    fetch_tag = Tags.objects.get(tagi=tagi_name[item])
                    new_post.tag.add(fetch_tag)
                    new_post.save()
                elif do_exist_tag(tagi_name[item]) == 0:
                    new_tag = Tags.objects.create(tagi=tagi_name[item])
                    new_tag.save()
                    new_post.tag.add(new_tag)
                    new_post.save()
            return new_post.id

        elif choice == False:
            new_post = Post(title=title, content=content, author=author, publish=choice, event=event)
            new_post.save()
            for item in range(len(tagi_name)):
                if do_exist_tag(tagi_name[item]) == 1:
                    fetch_tag = Tags.objects.get(tagi=tagi_name[item])
                    new_post.tag.add(fetch_tag)
                    new_post.save()
                elif do_exist_tag(tagi_name[item]) == 0:
                    new_tag = Tags.objects.create(tagi=tagi_name[item])
                    new_tag.save()
                    new_post.tag.add(new_tag)
                    new_post.save()
            return new_post.id


    def add_tag_to_post(self, tag_name, post_id):
        retri_post = Post.objects.get(id=post_id)
        new_tags = Tags.objects.create(tagi=tag_name)
        retri_post.tag.add(new_tags)
        retri_post.save()

    def add_existing_tag_to_post(self, post_id, tag_id):
        retri_post = Post.objects.get(id=post_id)
        retri_tag = Tags.objects.get(id=tag_id)
        retri_post.tag.add(retri_tag)
        retri_post.save()
        retri_tag.save()

    def remove_tag_from_post(self, post_id, tag_id):
        retri_post = Post.objects.get(id=post_id)
        retri_tag = Tags.objects.get(id=tag_id)
        retri_post.tag.remove(retri_tag)
        retri_post.save()
        retri_tag.save()

    def delete_post_by_id(self, id):
        instance = Post.objects.get(id=id)
        instance.delete()

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

    #mutlimedia
    def delete_multimedia_by_id(self, id):
        retri = Multimedia.objects.get(id=id)
        retri.delete()

    def retrive_mutlimedia(self):
        retri = Multimedia.objects.all()
        return retri.photos.url
    #commments
    def comments_of_post(self, post_id):
        retri_comm = Comment.objects.filter(post_id=post_id).values()
        return retri_comm

    def retrive_comments_by_id(self, id):
        retri = Comment.objects.get(id=id)
        return retri

    def delete_comment_by_id(self, id):
        retri = Comment.obejects.get(id=id)
        retri.delete()

    def modify_comment_by_id(self, id, content):
        comm = Comment.objects.get(id=id)
        comm.content = content
        comm.save()

    #galeria
    def delete_from_gelery(self, id_gal, id_photo):
        gall = Galery.objects.get(id=id_gal)
        photo_instance= gall.multimedia_set.get(id=id_photo)
        photo_instance.delete()
        gall.save()
        photo_instance.save()

    def add_to_gallery(self, id_gal, id_photo):
        gall = Galery.objects.get(id=id_gal)
        ph_ins = Multimedia.objects.get(id=id_photo)
        gall.multimedia_set.add(ph_ins)
        gall.save()

    #formularz
    def new_registration(self, nick, name, surname, email, number, wydzial, kierunek, rok):
        new_member = Registration(nick=nick,
                                  name=name,
                                  surname=surname,
                                  number=number,
                                  email=email,
                                  wydzial=wydzial,
                                  kierunek=kierunek,
                                  rok=rok)
        new_member.save()

    def return_mails_of_users(self):
        data = Registration.objects.all()
        return list(data.email)


    def list_of_members(self):
        members = Registration.objects.values()
        return list(members)



