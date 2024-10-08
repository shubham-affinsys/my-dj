# Generated by Django 5.0.7 on 2024-08-23 09:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0015_todo_user_alter_todo_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='todo',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
