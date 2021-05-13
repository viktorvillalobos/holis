from model_bakery import baker

baker.generators.add(
    "apps.utils.fields.LowerCharField", "model_bakery.random_gen.gen_string"
)
