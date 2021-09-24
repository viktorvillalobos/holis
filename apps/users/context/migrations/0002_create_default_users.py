from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations

import datetime as dt
import uuid

# This migration was moved to 0014 after adding UUID

class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial"), ("core", "0003_create_default_company")]

    operations = []
