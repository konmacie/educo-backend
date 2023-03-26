# Generated by Django 4.1.5 on 2023-03-26 09:23

import apps.records.models.student
import apps.records.models.teacher
import apps.records.models.user
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('records.user',),
            managers=[
                ('objects', apps.records.models.student.StudentManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('records.user',),
            managers=[
                ('objects', apps.records.models.teacher.TeacherManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.records.models.user.CustomUserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Student'), (2, 'Teacher'), (3, 'Secretary'), (4, 'Admin')], default=1, editable=False, verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth date')),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='Address')),
                ('zip_code', models.CharField(blank=True, max_length=10, verbose_name='ZIP code')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='City')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Phone number')),
                ('student', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='records.student')),
            ],
        ),
    ]
