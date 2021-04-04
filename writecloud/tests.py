from django.test import TestCase

from writecloud.models import Story, Page, Review, User


class StoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Test_name', email='', password='0000')
        Story.objects.create(title='First_Test_Story', subtitle='This is the first test story', length='2', author=User.objects.last())

    def test_title_label(self):
        story = Story.objects.last()
        field_label = story._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_subtitle_label(self):
        story = Story.objects.last()
        field_label = story._meta.get_field('subtitle').verbose_name
        self.assertEqual(field_label, 'subtitle')

    def test_title_length(self):
        story = Story.objects.last()
        max_length = story._meta.get_field('title').max_length
        self.assertEqual(max_length, 30)

    def test_subtitle_length(self):
        story = Story.objects.last()
        max_length = story._meta.get_field('subtitle').max_length
        self.assertEqual(max_length, 60)

    def test_author_correct(self):
        story = Story.objects.last()
        expected_object_name = User.objects.last()
        self.assertEqual(expected_object_name, story.author)

    def test_length(self):
        story = Story.objects.last()
        self.assertEqual(story.length, 2)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Test_name1', email='', password='0000')

    def test_username(self):
        user = User.objects.last()
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_password(self):
        user = User.objects.last()
        field_label = user._meta.get_field('password').verbose_name
        self.assertEqual(field_label, 'password')


class PageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Another_test', email='', password='0000')
        Story.objects.create(title='First_Test_Story', subtitle='This is the first test story', length='2', author=User.objects.last())
        Page.objects.create(content='Test_Content', story=Story.objects.last(), author=User.objects.last(), number='1')

    def test_number(self):
        page = Page.objects.last()
        field_label = page._meta.get_field('number').verbose_name
        self.assertEqual(field_label, 'number')

    def test_content(self):
        page = Page.objects.last()
        field_label = page._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_author(self):
        page = Page.objects.last()
        field_label = page._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_story(self):
        page = Page.objects.last()
        field_label = page._meta.get_field('story').verbose_name
        self.assertEqual(field_label, 'story')

    def test_author_constraint(self):
        try:
            Page.objects.create(content='Test_Content', story=Story.objects.last(), author=User.objects.first(), number='2')
        except Exception as e:
            self.assertEqual(str(e), 'UNIQUE constraint failed: writecloud_page.story_id, writecloud_page.author_id')


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Test_name', email='', password='0000')
        Story.objects.create(title='First_Test_Story', subtitle='This is the first test story', length='2',
                             author=User.objects.last())
        User.objects.create_user(username='Test_name1', email='', password='0000')
        Review.objects.create(stars ='4', body='Great one', author=User.objects.last(), story=Story.objects.last())

    def test_stars(self):
        review = Review.objects.last()
        field_label = review._meta.get_field('stars').verbose_name
        self.assertEqual(field_label, 'stars')

    def test_body(self):
        review = Review.objects.last()
        field_label = review._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_story(self):
        review = Review.objects.last()
        field_label = review._meta.get_field('story').verbose_name
        self.assertEqual(field_label, 'story')

    def test_author(self):
        review = Review.objects.last()
        field_label = review._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')
