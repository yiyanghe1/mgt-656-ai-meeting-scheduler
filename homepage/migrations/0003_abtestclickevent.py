from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_abtestevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbTestClickEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(db_index=True, max_length=40)),
                ('variant', models.CharField(choices=[('kudos', 'Kudos'), ('thanks', 'Thanks')], max_length=10)),
                ('user_agent', models.CharField(blank=True, max_length=255)),
                ('ip_address', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'abtest_click_events',
                'ordering': ['-created_at'],
            },
        ),
    ]
