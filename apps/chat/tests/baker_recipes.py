from model_bakery.recipe import Recipe, related

from apps.core.tests import baker_recipes as core_recipes
from apps.users.tests import baker_recipes as user_recipes
from apps.utils.baker import get_or_create_foreign_key

adslab_room_one_to_one = Recipe(
    "chat.Room",
    company=get_or_create_foreign_key(core_recipes.adslab),
    name="viktor",
    is_one_to_one=True,
    any_can_invite=False,
    members_only=True,
    max_users=2,
    members=related(user_recipes.user_viktor, user_recipes.user_julls),
)


adslab_message_one_to_one = Recipe(
    "chat.Message",
    company=get_or_create_foreign_key(core_recipes.adslab),
    room=get_or_create_foreign_key(adslab_room_one_to_one),
    user=get_or_create_foreign_key(user_recipes.user_viktor),
    text="Hello Julls",
)

adslab_attachment_one_to_one = Recipe(
    "chat.MessageAttachment",
    company=get_or_create_foreign_key(core_recipes.adslab),
    message=get_or_create_foreign_key(adslab_message_one_to_one),
    _create_files=True,
)
