import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.develop')
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

os.system('mkdir -p mediafiles/tours/')
os.system('cp seed.jpg mediafiles/tours/seed.jpg')

from django_seed import Seed
from random import randint

seeder = Seed.seeder()

from categories.models import Category
from django.contrib.auth.models import User

user, res = User.objects.get_or_create(
    pk=1,
    username='admin',
)
user.set_password('admin')


def seed_category(count=5):
    seeder.add_entity(Category, count, {
        'thumbnail': None,
        'name': seeder.faker.name(),
    })
    seeder.execute()


def seed_tours(count=5):
    from apps.tour.models import Tour, TourDays, TourPhotos

    seeder.add_entity(Tour, count, {
        'title': lambda x: seeder.faker.name(),
        'slug': lambda x: seeder.faker.name().replace(' ', '-'),
        'priority': None,
        'price': lambda x: randint(500, 8000),
    })

    res = seeder.execute()
    for t in res[Tour]:
        t = Tour.objects.get(id=t)
        t.categories.set(Category.objects.order_by('?')[:2])
        seeder.add_entity(TourPhotos, 1, {
            'photo': 'tours/seed.jpg',
            'tour': t,
            'title': lambda x: seeder.faker.country(),
        })

        seeder.add_entity(TourDays, 3, {
            'tour': t,
        })

    seeder.execute()


def seed_posts(count=5):
    from apps.post.models import Post

    seeder.add_entity(Post, count, {
        'author': User.objects.first(),
        'photo': 'tours/seed.jpg',
    })
    res = seeder.execute()
    for t in res[Post]:
        t = Post.objects.get(id=t)
        t.categories.set(Category.objects.order_by('?')[:2])


seed_category(10)
seed_tours(10)
seed_posts(10)
