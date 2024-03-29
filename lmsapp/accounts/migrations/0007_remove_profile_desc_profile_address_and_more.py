# Generated by Django 5.0.2 on 2024-03-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_remove_feedback_course_remove_feedback_student_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="desc",
        ),
        migrations.AddField(
            model_name="profile",
            name="address",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_pic",
            field=models.ImageField(default="default.jpg", upload_to="profile_pic"),
        ),
    ]
