# Generated by Django 3.2.2 on 2022-05-07 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ATransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('C', 'COIN_TRANSACTION'), ('F', 'FILE_TRANSACTION')], max_length=1)),
                ('account_from', models.CharField(max_length=1000)),
                ('account_to', models.CharField(max_length=1000)),
                ('transaction_data', models.CharField(max_length=1000)),
                ('transaction_fees', models.IntegerField()),
                ('signature', models.CharField(max_length=1000)),
                ('status', models.CharField(choices=[('P', 'PENDING'), ('A', 'APPROVED')], default='P', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_public_key', models.CharField(max_length=1000)),
                ('issuer_public_key', models.CharField(max_length=1000)),
                ('valid_till', models.IntegerField(default=0)),
                ('valid_from', models.IntegerField(default=0)),
                ('signature', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionSummaryBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accounts_from', models.JSONField()),
                ('accounts_to', models.JSONField()),
                ('included_transactions', models.ManyToManyField(to='core.ATransaction')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionLinkNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.transactionlinknode')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.atransaction')),
            ],
        ),
        migrations.CreateModel(
            name='Peer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=1000)),
                ('familiarity', models.IntegerField(default=0)),
                ('ip_address', models.CharField(max_length=1000)),
                ('port', models.IntegerField(default=0)),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.certificate')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
                ('nonce', models.IntegerField(default=0)),
                ('file_hash', models.CharField(max_length=1000)),
                ('transaction_hash', models.CharField(max_length=1000)),
                ('prev_block_hash', models.CharField(max_length=1000)),
                ('transaction_summary_hash', models.CharField(max_length=1000)),
                ('data', models.CharField(max_length=10000)),
                ('difficulty', models.IntegerField()),
                ('number', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('M', 'Mined'), ('C', 'Confirmed')], default='P', max_length=1)),
                ('block_number', models.IntegerField(default=0)),
                ('miner', models.CharField(blank=True, max_length=1000, null=True)),
                ('transaction_summary_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.transactionsummaryblock')),
            ],
        ),
        migrations.CreateModel(
            name='AccountHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=1000)),
                ('balance', models.IntegerField(default=0)),
                ('certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.certificate')),
            ],
        ),
    ]
