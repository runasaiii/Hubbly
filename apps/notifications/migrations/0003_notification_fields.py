# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_deleted_at_notification_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('comment', 'Comment'), ('like', 'Like'), ('follow', 'Follow'), ('event', 'Event'), ('community', 'Community'), ('post', 'Post')], default='post', max_length=20),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_object_id',
            field=models.UUIDField(blank=True, help_text='ID связанного объекта (пост, комментарий, событие и т.д.)', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_object_type',
            field=models.CharField(blank=True, help_text='Тип связанного объекта (post, comment, event и т.д.)', max_length=50),
        ),
    ]

