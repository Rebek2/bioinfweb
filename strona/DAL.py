from .models import Tags, Post, Multimedia, Comment, Galery, Registration, Downloadable, Members
import os
import sqlite3
from pathlib import Path
from bioinfweb import settings

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

    def fetch_tags(self, do_all, tag_id=0):
        if do_all is True:
            retri = Tags.objects.all()
            return retri
        elif do_all is False:
            retrival = Tags.objects.get(id=tag_id)
            return retrival
        else:
            raise ValueError("Choice must be boolean, True to retrive all tags or False to retrive one by id")

    def clear_unused_tags(self):
        fetch_tags = list(item.id for item in Tags.objects.all())
        con = sqlite3.connect(r"\bioinfweb\db.sqlite3")
        curr = con.cursor()
        rek = curr.execute("SELECT tags_id FROM strona_post_tag")
        post_tags = list(set(rek.fetchall()))
        for item in range(len(post_tags)):
            char = post_tags[item][0]
            post_tags[item] = char

        for tag in fetch_tags:
            if tag not in post_tags:
                ghost_tag = Tags.objects.get(id=tag)
                ghost_tag.delete()
        return None

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

    def fetch_post_values(self, post_id):
        post = Post.objects.get(id=post_id)
        tagi = Tags.objects.filter(post=post_id)
        redable_tags = ""
        for item in range(len(tagi)):
            if item == len(tagi)-1:
                redable_tags = redable_tags + f"{tagi[item]}"
            else:
                redable_tags = redable_tags + f"{tagi[item]},"
        mess = f"{post.title}\n{post.content}\n{redable_tags}\n{post.author}"

        return mess

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
    def add_comms_from_FB(self, dats, post_fb_id):
        try:
            post = Post.objects.get(facebook_id=post_fb_id)#that way, unpublished post wont be used
        except:
            return "Post is hidden or don't exist"
        fetch_comments = Comment.objects.filter(post_id=post.id)
        zip_comments = list((fetch_comments[item].User, fetch_comments[item].content)for item in range(len(fetch_comments)))
        comms = dats['comments']['data']
        fb_coms = list((comms[item]['from']['name'], comms[item]['message']) for item in range(len(comms)))
        for item in fb_coms:
            if item not in zip_comments:
                new_com = Comment(User=item[0], content=item[1], post_id=post.id)
                new_com.save()

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
    def new_registration(self, nick, name, surname, email, number, wydzial, kierunek, rok, subscription):
        new_member = Registration(nick=nick,
                                  name=name,
                                  surname=surname,
                                  number=number,
                                  email=email,
                                  wydzial=wydzial,
                                  kierunek=kierunek,
                                  rok=rok,
                                  subscription=subscription)
        new_member.save()
#members

    def return_mails_of_users(self):
        data = Registration.objects.all()
        data2 = Members.objects.all()
        mails = list(map(lambda x: x.email, data2))
        fetch_mails = []
        for record in data:
            if record.subscription == True:
                fetch_mails.append(record.email)

        return list(set(fetch_mails + mails))

    def fetch_club_court_mails(self):
        return list(map(lambda x: x.email, Members.objects.all()))


    def list_of_members(self):
        members = Registration.objects.values()
        return list(members)

    def change_subs_status(self, email_adres):
        try:
            instance = Registration.objects.get(email=email_adres)
        except:
            return "No such email adress in database"
        if instance.subscription == True:
            instance.subscription = False
            instance.save()
            return "Successfully changed subscription status"
        elif instance.subscription == False:
            return "Subscription is already aborted"

    def downloads_add(self, name, upload):
        parsed_upload_name = str(upload).replace(' ', '_')

        if len(Downloadable.objects.filter(name=name)) > 0:
            status = "File with such title already exist, its recomended to delete this file with same title."
            return status
        elif len(Downloadable.objects.filter(name=name)) <= 0:
            new_upload = Downloadable(name=name, upload=upload)
            new_upload.save()
            if parsed_upload_name in os.listdir(os.path.join(settings.MEDIA_ROOT, "uploads/")):
                warn = "File saved. Warning, name of files was were identical."
                return warn
            else:
                status = "File saved"
                return status


    def downloadable_fetch_all(self):
        files = Downloadable.objects.all()
        return files

    def downloads_edit(self, id, upload):
        file = Downloadable.objects.get(id=id)
        file.upload = upload
        file.save()
        #deletion of no longer usefule files
        files_in_uploads = os.listdir(os.path.join(settings.MEDIA_ROOT, 'uploads'))
        all_files = Downloadable.objects.all().values()
        all_files_lis = list(name['upload'].split(r'/')[1] for name in all_files)
        for file in files_in_uploads:
            if file not in all_files_lis:
                os.remove(os.path.join(settings.MEDIA_ROOT, 'uploads', file))
        status = "Changes saved"
        return status

    def downloads_counter(self, id):
        file = Downloadable.objects.get(id=id)
        file.downloads = file.downloads + 1
        file.save()

    def downloads_delete(self, id):
        try:
            file = Downloadable.objects.get(id=id)
            name = str(file.upload.name).split(r'/')
            if name[1] in os.listdir(os.path.join(settings.MEDIA_ROOT, 'uploads')):
                os.remove(os.path.join(settings.MEDIA_ROOT, 'uploads', file.upload.name))
            else:
                status = "No such file in database"
                return status
            file.delete()  # test
            status = 'File deleted'
            return status
        except:
            status = "File do not exist!"

            #return status