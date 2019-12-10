# Generated by Django 2.2.7 on 2019-11-24 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartmodels.models.smart


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.SMARTMODELS_NAMESPACE_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('bio', models.TextField(verbose_name='Biography')),
                ('created_by', models.ForeignKey(blank=True, help_text='Creator (owner) of the resource.', null=True, on_delete=models.SET(smartmodels.models.smart.get_sentinel_user), related_name='accounts_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET(smartmodels.models.smart.get_sentinel_user), related_name='accounts_deleted', to=settings.AUTH_USER_MODEL)),
                ('namespaces', models.ManyToManyField(help_text='Visibility domain: org, district, domain, etc.', related_name='accounts_owned', to=settings.SMARTMODELS_NAMESPACE_MODEL)),
                ('owner', models.ForeignKey(blank=True, help_text='User obo. whom this resource is created. The sentinel owner on deletion.', null=True, on_delete=models.SET(smartmodels.models.smart.get_sentinel_user), related_name='accounts_owned', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET(smartmodels.models.smart.get_sentinel_user), related_name='accounts_updated', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
