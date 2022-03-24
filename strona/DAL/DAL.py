from strona.models import Tags


class Database:
    def add_tag(self, tag_name):
        t = Tags(name=tag_name)
        t.save()

    def retrieve_tag(self, tag_id):
        retval = Tags.objects.filter(id=tag_id).values('title')

        for x in retval:
            return x['title']

    def modify_tag_name_by_id(self, id, name):
        pass