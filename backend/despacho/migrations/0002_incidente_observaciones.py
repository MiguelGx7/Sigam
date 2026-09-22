from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despacho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incidente',
            name='estado_incidente',
            field=models.CharField(
                blank=True,
                choices=[
                    ('en_espera', 'En espera'),
                    ('llegada_incidente_confirmada', 'Llegada al incidente confirmada'),
                    ('observaciones_registradas', 'Observaciones registradas'),
                    ('traslado_iniciado', 'Traslado iniciado'),
                    ('hospital_seleccionado', 'Hospital seleccionado'),
                    ('llegada_hospital_confirmada', 'Llegada al hospital confirmada'),
                    ('cerrado', 'Cerrado'),
                ],
                default='en_espera',
                max_length=50,
                null=True,
            ),
        ),
    ]
