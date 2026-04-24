from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_lead_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='preferred_location',
            field=models.CharField(
                choices=[('chandigarh','Chandigarh'),('mohali','Mohali'),('zirakpur','Zirakpur'),('panchkula','Panchkula'),('kharar','Kharar'),('haryana','Haryana (Other)'),('other','Other Location')],
                default='mohali',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='lead',
            name='budget',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='property_interest',
            field=models.CharField(
                choices=[('flat','Flat / Apartment'),('room','Room / PG / Studio'),('plot','Residential Plot'),('villa','Independent Villa / House'),('commercial','Commercial Space / Shop / Office'),('building','Building / Complex'),('farm','Farm House / Agricultural Land'),('other','Other')],
                default='flat',
                max_length=50,
            ),
        ),
    ]
