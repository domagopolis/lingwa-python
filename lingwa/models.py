from django.db import models

class Url(models.Model):
    url = models.CharField(max_length=200)
    last_read = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.url

class Image(models.Model):
    src = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.src

class Language(models.Model):
    name = models.CharField(max_length=200)
    iso3letter = models.CharField(max_length=3)
    iso2letter = models.CharField(max_length=2)
    popular = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Utterence(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    utterence = models.TextField()
    count = models.IntegerField(default=1)
    translations = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.utterence

    def __unicode__(self):
        return u"%s" % self.utterence

class LexicalClass(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'lexical class'
        verbose_name_plural = 'lexical classes'

    def __str__(self):
        return self.name

class Keyword(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=200)
    count = models.IntegerField(default=1)
    lexical_definitions = models.ManyToManyField(LexicalClass, through='LexicalDefinition', related_name='keywords')

    def __str__(self):
        return self.keyword

    def __unicode__(self):
        return u"%s" % self.keyword

class KeywordUrl(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    url = models.ForeignKey(Url, on_delete=models.CASCADE)

    def __str__(self):
        return '{0.url!s} ({0.keyword!s})'.format(self)

class LexicalDefinition(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    lexical_class = models.ForeignKey(LexicalClass, on_delete=models.CASCADE)
    translations = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return u'{0.keyword!s} [{0.lexical_class!s}] ({0.keyword.language!s})'.format(self)
