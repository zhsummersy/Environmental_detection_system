from django.db import models
from datetime import datetime  

# 用户模型
class webuser(models.Model):
    # 用户名
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,blank=False,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=30,blank=False,verbose_name='密码')
    email = models.CharField(max_length=30,blank=False,verbose_name='邮箱')
    age = models.IntegerField(verbose_name='年龄')
    hobby = models.CharField(max_length=30,blank=False,verbose_name='爱好')
    kind = models.CharField(max_length=30,blank=False,verbose_name='性格') # 类型:运动、休闲、舒适、激烈
    def __str__(self):
        return self.username
    class Meta:  
        verbose_name = '用户'
        verbose_name_plural = '用户'

# 检测指标
class Metric(models.Model): 
    Metricid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255,blank=False,verbose_name='指标名称')  
    unit = models.CharField(max_length=50,blank=False,verbose_name='指标单位')  
    purpose = models.TextField(verbose_name='指标用途')  
  
    def __str__(self):  
        return self.name
    class Meta:  
        verbose_name = '检测指标'
        verbose_name_plural = '检测指标'
# 检测点
class DetectionPoint(models.Model):  
    id = models.AutoField(primary_key=True)  
    num = models.CharField(max_length=255,verbose_name='编号')
    name = models.CharField(max_length=255,verbose_name='检测点名称')  
    location = models.CharField(max_length=255,verbose_name='检测点位置')  
  
    def __str__(self):  
        return self.name
    class Meta:  
        verbose_name = '检测点'
        verbose_name_plural = '检测点'
# 报警
class Alert(models.Model):  
    Alertid = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=datetime.now,verbose_name='警报日期')  
    content = models.CharField(max_length=255,verbose_name='警报内容')  
    value = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='警报值')  
  
    def __str__(self):  
        return f'{self.datetime} - {self.content}: {self.value}'
    class Meta:  
        verbose_name = '警报清单'
        verbose_name_plural = '警报清单'
# 阈值
class Threshold(models.Model):  
    id = models.AutoField(primary_key=True)  # 主键ID  
    indicator = models.CharField(max_length=255,verbose_name='指标名称')  # 指标  
    indicator_id = models.CharField(max_length=255,verbose_name='指标ID')  # 指标ID  
    threshold = models.DecimalField(max_digits=10, decimal_places=4,verbose_name='阈值')  # 阈值  
  
    def __str__(self):  
        return f'Threshold: {self.indicator}, Indicator ID: {self.indicator_id}, Threshold Value: {self.threshold}'
    class Meta:  
        verbose_name = '阈值设定'
        verbose_name_plural = '阈值设定'
# 上报数据
class SensorData(models.Model):  
    id = models.AutoField(primary_key=True)  # 主键ID  
    co_concentration = models.DecimalField(max_digits=5, decimal_places=4,verbose_name='一氧化碳浓度')  # 一氧化碳浓度  
    h2s_concentration = models.DecimalField(max_digits=5, decimal_places=4,verbose_name='硫化氢浓度')  # 硫化氢浓度  
    methane_concentration = models.DecimalField(max_digits=5, decimal_places=4,verbose_name='甲烷浓度')  # 甲烷浓度  
    ammonia_concentration = models.DecimalField(max_digits=5, decimal_places=4,verbose_name='氨气浓度')  # 氨气浓度  
    water_level = models.DecimalField(max_digits=5, decimal_places=4,verbose_name='水位高度')  # 水位高度  
    report_time = models.DateTimeField(default=datetime.now)  # 上报时间  

    def save(self, *args, **kwargs):  
        if not self.report_time:  
            self.report_time = datetime.now()  
        super().save(*args, **kwargs)
    def __str__(self):  
        return f'ID: {self.id}, CO: {self.co_concentration}, H2S: {self.h2s_concentration}, Methane: {self.methane_concentration}, Ammonia: {self.ammonia_concentration}, Water Level: {self.water_level}, Report Time: {self.report_time}'
    class Meta:  
        verbose_name = '上报数据'
        verbose_name_plural = '上报数据'

# 风机状态
class Fan(models.Model): 
    id = models.AutoField(primary_key=True)  
    zt = models.TextField(verbose_name='风机状态')  
  
    def __str__(self):  
        return self.zt
    class Meta:  
        verbose_name = '风机状态'
        verbose_name_plural = '风机状态'