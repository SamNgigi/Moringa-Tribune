"""
We import the models class from the 'django.db' modules.

A models is basically a python class that inherits from the
'modules.Model' class
"""
from django.db import models
import datetime as dt

# Create your models here.


class Editor(models.Model):
    """
    We create the Editor class that inherits from the modules.

    We then create three classs variables that represent different
    columns in our database.

    We use Field objects to define what sort of data the database will store.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    # 'blank=True' this allows us to add Null values to our database
    phone_number = models.CharField(max_length=10, blank=True)

    """
    We add an __str__ function that will return a string
    representation of our model.

    This will be useful  when we watn to view our returned queries
    """

    def __str__(self):
        return self.first_name

    # The save method
    def save_editor(self):
        self.save()

    def delete_editor(self):
        self.delete()

    """
    Changed
    ordering = ['name']
    to
    ordering = ['first_name'],

    Removed below error
        SystemCheckError: System check identified some issues:
        ERRORS:
        news.Editor: (models.E015) 'ordering' refers to the
        non-existent field 'name'.
    """
    class Meta:
        ordering = ['first_name']


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    # The save method
    def save_tag(self):
        self.save()

    def delete_tag(self):
        self.delete()


class Article(models.Model):
    """
    Defining the Articles class.

    This model has a one to many relationship between articles and the editor.
        An article has one editor... but one editor can edit multiple articles

    This model also has a many to many relationship between articles and tags.
        -A single article can have may tags and a single tag can
        be shared by multiple articles

    To get the dates when an article was posted we add a timespamp to our model
    """
    title = models.CharField(max_length=60)
    body = models.TextField()
    editor = models.ForeignKey(Editor)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    # blank=True allows  to continue with article image as null for now.
    article_image = models.ImageField(upload_to='articles/', blank=True)

    # The save method
    def save_article(self):
        self.save()

    # The delete method
    def delete_article(self):
        self.delete()

    @classmethod
    def todays_news(cls):
        """
        We use the Django query filter date that allows us to convert
        out datetimefield to a date.

        Note the twwo underscores after the first date.
        """
        today = dt.date.today()
        news = cls.objects.filter(pub_date__date=today)
        return news

    @classmethod
    def date_news(cls, date):
        news = cls.objects.filter(pub_date__date=date)
        return news

    @classmethod
    def search_by_title(cls, search_term):
        """
        This is a method that will help us fileter all the Articles in
        our database and return one matching a search query.

        This search query is passed in as search_term the second
        argument in our method.

        We use the __icontains query filter that checks if any word in
        the title field of our articles matches the search term.

        We return the result.
        """
        news = cls.objects.filter(title__icontains=search_term)
        return news
