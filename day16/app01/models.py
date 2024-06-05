from django.db import models
from django.core import validators
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    '''部门表'''
    title = models.CharField(max_length=40,verbose_name='部门标题')

class UserInfo(models.Model):
    '''员工表'''    
    name = models.CharField(max_length=40,verbose_name='员工姓名')
    login_account = models.CharField(max_length=30,verbose_name='登录账号')
    password = models.CharField(max_length=40,verbose_name='登录密码')
    age = models.IntegerField(verbose_name='员工年龄')
    account = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2)
    create_time = models.DateTimeField(verbose_name='注册时间',default=timezone.now)
    gender_choices=( (1,'男'), (2,'女'), )
    gender = models.SmallIntegerField(verbose_name='用户性别，1:男，2:女',choices=gender_choices)


    # 数据库无约束
    # depart_id = models.IntegerField(verbose_name='部门ID')
    # ForeignKey会给字段depart自动加上_id，自动生成depart_id
    # 支持级联删除， ,on_delete=models.CASCADE
    # 删除置空， null=True,blank=True,on_delete=models.SET_NULL | SET_DEFAULT
    depart = models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE)

class PrettyNum(models.Model):
    """ 靓号 """
    mobile = models.CharField(verbose_name="手机靓号",max_length=11,null=False,blank=False)
    price = models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2)
    level_choices = ((1,"钻石"),(2,"黄金"),(3,"白银"))
    level = models.IntegerField(verbose_name="级别",choices=level_choices,default=3)
    status_choices = ((0,"未占用"),(1,"占已用"))
    status = models.SmallIntegerField(verbose_name="靓号状态",choices=status_choices,default=0)

    # mobile_validators=[validators.RegexValidator(r"^\d{10}0$","手机尾号必须是0")]


'''
【Field】 类常见的参数：
verbose_name：字段的可读性名称，用于在 Django 的 Admin 界面中显示。
name：字段的实际名称，如果未指定，则默认使用属性名称。
db_column：指定数据库中列的名称，如果未指定，则默认使用字段的名称。
primary_key：指定该字段为主键，如果未指定，则 Django 会自动创建一个自增的整数主键。
unique：指定该字段的值是否唯一。
null：指定该字段是否可以为空值，默认为 False。
blank：指定在表单验证时该字段是否可以为空，默认为 False。
default：指定字段的默认值。
choices：用于创建具有预定义选项的字段，例如枚举类型。
max_length：指定字符字段的最大长度。
validators：指定用于验证字段值的验证器列表。
help_text：在 Admin 界面中为该字段提供帮助文本。
【DecimalField 】类常见的参数：
max_digits：表示数字允许的最大位数（包括小数点前和小数点后）。该参数必须大于或等于 decimal_places。
decimal_places：表示与数字一起存储的小数位数。
'''
