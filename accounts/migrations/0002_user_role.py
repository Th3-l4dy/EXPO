# Generated by Django 3.2 on 2023-05-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("student", "Student"),
                    ("supervisor", "Supervisor"),
                    ("company", "Company"),
                ],
                default=None,
                max_length=20,
                null=True,
            ),
        ),
    ]
