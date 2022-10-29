from .models import Tags, Post, Multimedia, Comment, Galery, Registration
import os

class Database:
    #tagi
    def add_tags(self, tags_names):
        fetch_tags = Tags.objects.all()
        lis_fetch_tags = list(str(item.tagi) for item in fetch_tags)
        tags_names.split(",")
        for tag in tags_names:
            if tag not in lis_fetch_tags:
                t = Tags(tagi=tag)
                t.save()

        fetch_new_tags = Tags.objects.all()
        return fetch_new_tags

    def fetch_tags(self, tag_id, do_all):
        if do_all is True:
            retri = Tags.objects.all()
            return retri
        elif do_all is False:
            retrival = Tags.objects.get(id=tag_id)
            return retrival
        else:
            raise ValueError("Choice must be boolean, True to retrive all tags or False to retrive one by id")

    def clear_unused_tags(self):
        fetch_tags = list(str(item.tagi) for item in Tags.objects.all())
        post = Post.objects.all()
        posts_tags = post.tag.all()
        return (fetch_tags, posts_tags)

    #posty
    def retrieve_post_by_id(self, id):
        retri = Post.objects.get(id=id)
        #fetch = Multimedia.objects.get(photos=file)
        #print(fetch)
        #for item in range(len(retri.photos.all())):
        #    print(str(retri.photos.all()[item].photos).split("photos/")[1])
        return retri

    def retrive_posts_values(self):
        retri = Post.objects.all().values().order_by("id")
        retri2 = Post.objects.all()[0].tag.all()
        all_data = (retri, retri2)
        return all_data

    def modify_post_by_id(self, id, tittle, content, author, event, tags, publish, files):
        new_post_content = Post.objects.get(id=id)
        new_post_content.publish = publish
        new_post_content.event = event
        #tags handling
        if len(tags) == 0:
            pass
        else:
            tags = tags.split(",")
            fetch_tags = Tags.objects.all()
            list_of_tags = list(str(item.tagi) for item in fetch_tags)
            fetch_post_tags = new_post_content.tag.all()
            list_of_posttags = list(str(item.tagi) for item in fetch_post_tags)
            for tag in tags:
                if tag not in list_of_posttags:
                    if tag not in list_of_tags:
                        new_tag = Tags.objects.create(tagi=tag)
                        new_tag.save()
                        new_post_content.tag.add(new_tag)
                        new_post_content.save()
                    elif tag in list_of_tags:
                        fetch_tag = Tags.objects.get(tagi=tag)
                        new_post_content.tag.add(fetch_tag)
                        new_post_content.save()

            for tag in list_of_posttags:
                if tag not in tags:
                    old_tag = Tags.objects.get(tagi=tag)
                    new_post_content.tag.remove(old_tag)
                    old_tag.save()
                    new_post_content.save()
        #rest of data
        if tittle != new_post_content.title:
            new_post_content.title = tittle

        if content != new_post_content.content:
            new_post_content.content = content

        if author != new_post_content.author:
            new_post_content.author = author

        #trying to figure out how to repair photos
        fetch_postfiles = [] #iteration before adding new photos
        for item in range(len(new_post_content.photos.all())):
            fetch_postfiles.append(str(new_post_content.photos.all()[item].photos).split("photos/")[1])

        raw_file_names = []
        for file in files:
            raw_file_names.append(str(file).replace(" ", "_"))

        for item in range(len(raw_file_names)):
            if raw_file_names[item] not in fetch_postfiles:
                new_photo = Multimedia(photos=files[item], post=new_post_content)
                new_photo.save()
                print(raw_file_names[item],True)
            else:
                print(raw_file_names[item], False)

        fetch_postfiles_new = [] #iteration after adding new photos
        for item in range(len(new_post_content.photos.all())):
            fetch_postfiles_new.append(str(new_post_content.photos.all()[item].photos).split("photos/")[1])

        for photo in fetch_postfiles_new:
            if photo not in raw_file_names:
                instance = Multimedia.objects.get(photos="photos/{}".format(photo))
                instance.delete()
                if os.path.exists(r"media/photos/{}".format(photo)):
                    os.remove(r"media/photos/{}".format(photo))
                print(instance.photos, 1)

            else:
                print(photo, 0)

        new_post_content.save()

    def remove_photo_instance(self, files, post_id):
        fetch = Multimedia.objects.get(photos=files)
        post = Post.objects.get(id=post_id)

        fetch_postfiles = []
        for item in range(len(post.photos.all())):
            fetch_postfiles.append(str(post.photos.all()[item].photos).split("photos/")[1])

        print(fetch.photos, fetch_postfiles)
        if str(fetch.photos).split("photos/")[1] in fetch_postfiles:
            print(True)
        else:
            print(False)

        for photo in files:
            if photo not in fetch_postfiles:
                photo_insta = Multimedia(photos=photo, post=post)
                photo_insta.save()

        for photo in fetch_postfiles:
            if photo not in files:
                print(photo)
                instance = "photos/{}".format(photo)
                old_photo = Multimedia.objects.get(photos=instance)
                #post.photos.remove(old_photo)
                post.photos.filter(photos=instance)
                old_photo.save()
                post.save()


        print(fetch.id, post.id)


    def do_exi_tag(self, tag):
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
        fetch_mails = []
        for email in data:
            fetch_mails.append(email.email)
        return fetch_mails


    def list_of_members(self):
        members = Registration.objects.values()
        return list(members)





