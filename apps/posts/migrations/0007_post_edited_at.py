# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

