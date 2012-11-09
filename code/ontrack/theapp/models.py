from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=200)
    

class User(models.Model):
    email = models.EmailField()
    user_name = models.CharField(max_length=200)
    join_time = models.BigIntegerField()
    weight = models.IntegerField()
    

class Link(models.Model):
    url = models.URLField()
    link_type = models.IntegerField()
    notes = models.TextField()
    
    date_added = models.BigIntegerField()
    who_added = models.ForeignKey(User)
    
    thumb = models.ImageField(upload_to="link_thumbs", null=True)


class Track(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    level = models.IntegerField(null=True)
    links = models.ManyToManyField(Link)
    tags = models.ManyToManyField(Tag)
    
    created_time = models.BigIntegerField()
    created_by = models.ForeignKey(User)
    unique_url = models.CharField(max_length = 200)


class Comment(models.Model):
    text = models.TextField()
    vote_type = models.IntegerField()
    
    user = models.ForeignKey(User)
    track = models.ForeignKey(Track)
    when = models.BigIntegerField()


class ShareLog(models.Model):
    where_to = models.IntegerField()
    when = models.BigIntegerField()
    user = models.ForeignKey(User)
    track = models.ForeignKey(Track)



###################
######## LOG - IN
###################
class Nonce(models.Model):
    """ Required for OpenID functionality """
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    def __unicode__(self):
        return u"Nonce: %s for %s" % (self.salt, self.server_url)


class Association(models.Model):
    """ Required for OpenID functionality """
    server_url = models.TextField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.TextField(max_length=255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length=64)

    def __unicode__(self):
        return u"Association: %s, %s" % (self.server_url, self.handle)

