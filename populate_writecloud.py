import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django

django.setup()
from random import randrange
from PIL import Image
from writecloud.models import Story, Page, UserProfile, Review, User


def populate():
    users = [
        {'username': ['Boris', 'George', 'Harry', 'Jack', 'Jacob', 'Naoh', 'Charlie', 'Mohammed', 'James', 'Henry',
                      'Olivia', 'Lily', 'Sophia', 'Emily', 'Amelia', "Ava", 'Isla', 'Isabella', 'Ella', 'Sophie'],
         'password': ['vfqtb00r', 'g2yqiiS7', '54JQm646', 'xnplwYHT', 'ltEjz24t', 'KvbNRbKH', 'wtIh9Of5', 'BoTnFyaF',
                      'Lm5Yru37', 'xVBbj9GF', 'T5EYnFSo', 'ZhIseIXW', 'f4TjGcSi', 'JiFUGzbU', 'O48AjjDJ', 'o2ksjSIV',
                      'Lm5Ydu37', 'xVabj9GF', 'T4EYnFSo', 'ZhsseIXW']}
    ]

    stories = [{
        'title': ['Titan Ticking', 'Dressed for Carnage', 'Signs of Life', 'Eternal Love', 'Defend the Past',
                  'Dream Boat', 'Heart of Thirst', 'The Fall', 'Built for Gold', 'Yesterday', 'Tonight',
                  'Another cup of coffee', 'Hurricane', 'Jubilee Street', 'I remember', 'The Chain', 'Spooky',
                  'Sunday Morning', 'Under my Thumb', 'White Room', 'The End', 'Election day', 'Apocalypse Now',
                  'Taxi Driver', 'The Return', 'New Start', 'Last Change', 'Nightcrawler', 'Seven',
                  'Gone with the Wind'],
        'subtitle': ['Albert Einstein On Movies', 'Guide To Cinema', 'The hidden mystery', 'Another round',
                     'Paris, Texas',
                     'Somebody to hear', 'You know something is happening', 'When you walk out', 'Nose on the ground',
                     'Wearing headphones', 'Cracking the code', 'Django is an old fashioned framework',
                     'Better use React',
                     'Don not be fooled', 'How experienced are you?', 'Famous Quotes', 'Best Advice',
                     'How to be successful',
                     'I saw them leaving', 'Call the cops', 'This happened yesterday', 'No luck', 'Contenders',
                     'Best bar in town', 'Generate password', 'Best musicians ever', 'No wars', 'Bring a bright future',
                     'One of the last', 'Sentenced to happiness'],
        'template': ['1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4',
                     '2', '3', '4', '1', '2', '3', '4', '1', '2', '1', '2', '1', '2'],
        'length': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4',
                   '2', '3', '4', '1', '2', '3', '4', '1', '2', '1', '2', '1', '2', '1', '2']
    }]

    page_content = ['The morning of June 27th was clear and sunny, with the fresh warmth of a full-summer day;',
                    'the flowers were blossoming profusely and the grass was richly green',
                    'The people of the village began to gather in the square, between the post office and the bank, '
                    'around ten clock',
                    'in some towns there were so many people that the lottery took two days and had to be started on '
                    'June 2th',
                    'but in this village, where there were only about three hundred people',
                    'the whole lottery took less than two hours',
                    'so it could begin at ten in the morning and still be through in time to allow the villagers '
                    'to get '
                    'home for noon dinner. ',
                    'The children assembled first, of course. School was recently over for the summer',
                    'and the feeling of liberty sat uneasily on most of them',
                    'they tended to gather together quietly for a while before they brokeinto boisterous play.',
                    'and their talk was still of the classroom and the teacher, of books and reprimands',
                    'Bobby Martin had already stuffed his pockets full of stones, and the other boys soon '
                    'followed his example',
                    'selecting the smoothest and roundest stones; Bobby and Harry Jones and Dickie Delacroix',
                    'the villagers pronounced this name Dellacroy',
                    'eventually made a great pile of stones in one corner of the square and guarded it '
                    'against the raids',
                    'The girls stood aside',
                    'talking among themselves',
                    'looking over their shoulders at rolled in the dust or clung to the hands of their older '
                    'brothers or sisters',
                    'Soon the men began to gather',
                    'surveying their own children',
                    'speaking of planting and rain',
                    'tractors and taxes',
                    'They stood together',
                    'away from the pile of stones in the corner',
                    'and their jokes were quiet and they smiled rather than laughed',
                    'The women, wearing faded house dresses and sweaters',
                    ', came shortly after their menfolk',
                    'They greeted one another and exchanged bits of gossip',
                    'as they went to join their husbands',
                    'Soon the women',
                    'standing by their husbands',
                    'began to call to their children',
                    'and the children came reluctantly',
                    'having to be called four or five times',
                    'Bobby Martin ducked under his mothers grasping hand and ran, laughing, back to the pile of stones',
                    'His father spoke up sharply',
                    'and Bobby came quickly',
                    'took his place between his father and his oldest brother',
                    'The lottery was conducted--as were the square dances',
                    'the teen club',
                    'the Halloween program',
                    'who had time and energy to devote to civic activities',
                    'He was a round-faced',
                    'jovial man and he ran the coal business',
                    'and people were sorry for him',
                    'because he had no children and his wife was a scold',
                    'When he arrived in the square',
                    'carrying the black wooden box',
                    'there was a murmur of conversation among the villagers',
                    'and he waved and called',
                    'followed him',
                    'carrying a three- legged stool,',
                    'and the stool was put in the center of the square',
                    'Summers set the black box down on it',
                    'The villagers kept their distance',
                    'leaving a space between themselves and the stool',
                    'there was a hesitation before two men',
                    'came forward to hold the box steady on the stool',
                    'while Mr. Summers stirred up the papers inside it. ']

    reviews_content = ['Nice one', 'Keep it up', 'Love it', 'Not good enough', 'Repetitive', 'Best story on the cloud',
                       'Neve heard that before', 'No way', 'Amazing', 'Cool', 'I thought I would also do that',
                       'Extremely motivational', 'Pure fiction', 'No coherence', 'I was there too', 'Did not like it',
                       'Pure lies', 'Only a fool would believe this story', 'Gotta be kidding me',
                       'I just do not agree',
                       'Come on', 'Just do it', 'Wow', 'Good luck friends', 'Every end is good', 'Barely read it',
                       'Boring', 'Meh', 'No surprise', 'No wonder', 'Just how', 'Do it again', 'Miss it']

    for i in range(len(users[0]['username'])):
        username = users[0]['username'][i]
        password = users[0]['password'][i]
        user = User.objects.create_user(username=username, email=None, password=password)
        user.save()

    for i in range(len(stories[0]['title'])):
        title = stories[0]['title'][i]
        subtitle = stories[0]['subtitle'][i]
        template = stories[0]['template'][i]
        length = stories[0]['length'][i]
        # First four stories will include images
        if i < 4:
            user = Story.objects.create(title=title, subtitle=subtitle, length=length, author=User.objects.all()[i],
                                        template=template, include_images=True)
        elif 4 <= i < 20:
            user = Story.objects.create(title=title, subtitle=subtitle, length=length, author=User.objects.all()[i],
                                        template=template, include_images=False)
        else:
            user = Story.objects.create(title=title, subtitle=subtitle, length=length,
                                        author=User.objects.all()[i - 20],
                                        template=template, include_images=False)
        user.save()

    # Set counters and get all images for populating
    content_max = len(page_content)
    k = 0
    images_counter = 0
    all_images = os.listdir(os.path.join(os.getcwd(), 'images_for_populate/'))
    while k < content_max - 1:
        for i in range(len(stories[0]['title'])):
            for j in range(int(stories[0]['length'][i])):
                number = j + 1
                story = Story.objects.all()[i]
                author = User.objects.all()[j]
                if k < content_max - 1:
                    content = page_content[k]
                    k += 1
                    if i < 4:
                        # Store images for population images folder to app media folder
                        with Image.open(os.path.join(os.getcwd(), 'images_for_populate/') + all_images[images_counter]) \
                                as image:
                            image.save(fp=os.path.join(os.getcwd(), 'media/') + all_images[images_counter])
                        page = Page.objects.create(number=number, content=content, story=story, author=author, image=
                        all_images[images_counter])
                        images_counter += 1
                        page.save()
                    else:
                        page = Page.objects.create(number=number, content=content, story=story, author=author)
                        page.save()

    counter = 0
    for i in range(7):
        for j in range(int(stories[0]['length'][i])):
            review_content = reviews_content[counter]
            counter += 1
            stars = randrange(1, 6)
            author = User.objects.all()[19 - j]
            story = Story.objects.all()[i]
            review = Review.objects.create(stars=stars, body=review_content, author=author, story=story)
            review.save()


if __name__ == '__main__':
    print('Starting Writecloud population script here...')
    populate()
