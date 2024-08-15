# Generated by Django 4.1.13 on 2024-07-24 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_remove_appointment_accepted_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.appointment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.doctor')),
            ],
        ),
    ]
