# Generated by Django 4.2.13 on 2024-06-03 05:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=40, verbose_name="部门标题")),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40, verbose_name="员工姓名")),
                (
                    "login_account",
                    models.CharField(max_length=30, verbose_name="登录账号"),
                ),
                ("password", models.CharField(max_length=40, verbose_name="登录密码")),
                ("age", models.IntegerField(verbose_name="员工年龄")),
                (
                    "account",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="账户余额"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="注册时间"
                    ),
                ),
                (
                    "gender",
                    models.SmallIntegerField(
                        choices=[(1, "男"), (2, "女")],
                        verbose_name="用户性别，1:男，2:女",
                    ),
                ),
                (
                    "depart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.department",
                    ),
                ),
            ],
        ),
    ]
