from django.conf import settings
from django.contrib.auth.models import User
from anansiapp.models import Deck, ClozeCard, ResponseCard, FavouriteDeck, Game, GamePlayer
from django_seed import Seed

# Create the seed data
seeder = Seed.seeder()

seeder.add_entity(User, 10, {
    'username': lambda x: seeder.faker.user_name(),
    'email': lambda x: seeder.faker.email(),
    'password': lambda x: seeder.faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
})

inserted_pks = seeder.execute()

seeder.add_entity(Deck, 10, {
    'user': lambda x: User.objects.get(pk=1),
    'name': lambda x: seeder.faker.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
    'privacy': lambda x: seeder.faker.random_element(elements=('public', 'private')),
})

inserted_pks = seeder.execute()

seeder.add_entity(ClozeCard, 10, {
    'deck': lambda x: Deck.objects.get(pk=1),
    'text': lambda x: seeder.faker.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
    'gap_index': lambda x: seeder.faker.random_int(min=0, max=10),
})

inserted_pks = seeder.execute()

seeder.add_entity(ResponseCard, 10, {
    'deck': lambda x: Deck.objects.get(pk=1),
    'text': lambda x: seeder.faker.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
})

inserted_pks = seeder.execute()
