from django.db import models


class Log(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    timestamp = models.DateTimeField()

    source = models.CharField(
        max_length=100
    )

    ip_address = models.CharField(
        max_length=100
    )

    event_type = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=50
    )

    username = models.CharField(
        max_length=100
    )

    raw_data = models.JSONField(
        null=True
    )

    processed = models.BooleanField(
        default=False
    )

    class Meta:

        db_table = "logs"

        managed = False