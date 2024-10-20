# Generated by Django 5.1.2 on 2024-10-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="completed_at",
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("completed", "Completed")],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
