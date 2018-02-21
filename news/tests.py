"""
Django provides a test module django.test where we import the TestCase class.

We then import our models
"""
from django.test import TestCase
from . models import Editor, Article, Tag
import datetime as dt
# Create your tests here.


class EditorTestClass(TestCase):
    # Set up method. Make sure to spell setUp correctly
    def setUp(self):
        self.test = Editor(first_name='Test',
                           last_name='Case', email='test@gmail.com')

    # Testing proper instantiation
    def test_instance(self):
        self.assertTrue(isinstance(self.test, Editor))

    # Testing save method
    def test_saving_editors(self):
        self.test.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)

    def test_deleting_editors(self):
        self.test = Editor(first_name='Test',
                           last_name='Case', email='test@gmail.com')
        self.test.save_editor()
        # self.test.save_editor()
        self.test.delete_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) < 1)


class ArticlesTestClass(TestCase):
    """
    Class to test the Article model.

    Since the Editor and Article share One to Many relationship we save
    the Editor instance first then equate it to the editor field in the
    Article model.

    For the many to many relationship we first save both the Tag and the
    Article instance. This allows us to have the id property of both
    that we can join in a db table.

    We then use the add function on the ManyToManyField to add a new tag.
    """
    # Set up method. Make sure to spell setUp correctly

    def setUp(self):
        # Creating new editor and saving
        self.test = Editor(first_name='Test',
                           last_name='Case', email='test@gmail.com')
        self.test.save_editor()

        # Creating a new tag and saving it.
        self.new_tag = Tag(name='Testing')
        self.new_tag.save()

        self.test_article = Article(title='Test Title',
                                    body='This is a test body',
                                    editor=self.test)
        self.test_article.save()
        self.test_article.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        Tag.objects.all().delete()
        Article.objects.all().delete()
    # Testing proper instantiation

    def test_instance(self):
        self.assertTrue(isinstance(self.test_article, Article))
        self.assertTrue(isinstance(self.test, Editor))

    # Testing save method
    def test_saving_articles(self):
        # self.test.save_editor()
        self.test_article.save_article()
        articles = Article.objects.all()
        self.assertTrue(len(articles) > 0)

    def test_deleting_articles(self):

        self.test_article.save_article()
        # self.test.save_editor()
        self.test_article.delete_article()
        articles = Article.objects.all()
        self.assertTrue(len(articles) < 2)

    # Test to get today's news
    def test_get_news_today(self):
        today_news = Article.todays_news()
        self.assertTrue(len(today_news) > 0)

    def test_get_news_by_date(self):
        test_date = '2017-03-28'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.date_news(date)
        self.assertTrue(len(news_by_date) == 0)


class TagsTestClass(TestCase):
    # Set up method. Make sure to spell setUp correctly
    def setUp(self):
        self.test = Editor(first_name='Test',
                           last_name='Case', email='test@gmail.com')
        self.test.save_editor()

        self.test_article = Article(title='Test Title',
                                    body='This is a test body',
                                    editor=self.test)
        self.test_article.save_article()

        self.tag_test = Tag(name='Testing')

    # Testing proper instantiation
    def test_instance(self):
        self.assertTrue(isinstance(self.test, Editor))
        self.assertTrue(isinstance(self.test_article, Article))
        self.assertTrue(isinstance(self.tag_test, Tag))

    # Testing save method
    def test_save_tags(self):
        # self.test.save_editor()
        self.tag_test.save_tag()
        tags = Tag.objects.all()
        self.assertTrue(len(tags) > 0)

    def test_deleting_tags(self):
        self.tag_test = Tag(name='Testing')
        self.tag_test.save_tag()
        # self.test.save_editor()
        self.tag_test.delete_tag()
        tags = Tag.objects.all()
        self.assertTrue(len(tags) < 1)
