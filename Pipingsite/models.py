from django.db import models

# Create your models here.
class Info(models.Model):
    line_number = models.CharField(max_length=255)
    location = models.TextField()
    from_start = models.TextField()
    to = models.TextField()
    drawing_number = models.TextField()
    service = models.TextField()
    material = models.TextField()
    inservice_date = models.DateField()
    pipe_size = models.IntegerField()
    original_thickness = models.FloatField()
    stress = models.IntegerField()
    joint_efficiency = models.IntegerField()
    ca = models.IntegerField()
    design_life = models.IntegerField()
    design_pressure = models.IntegerField()
    operating_pressure = models.IntegerField()
    design_temperature = models.IntegerField()
    operating_temperature = models.FloatField()
    
    class Meta:
        verbose_name_plural = "Info"

    def __str__(self):
        return "ln: " + self.line_number

class CML(models.Model):
    line_number = models.ForeignKey(Info, on_delete=models.CASCADE, default=None, verbose_name="Info")
    cml_number = models.IntegerField()
    cml_description = models.TextField()
    actual_outside_diameter = models.FloatField(default=0.0)
    design_thickness = models.FloatField(default=0.0)
    structural_thickness = models.FloatField(default=0.0)
    require_thickness = models.FloatField(default=0.0)

    @property
    def get_actual_outside(self):
        outside = {
                0.125:10.300,
                0.250:13.700,
                0.357:17.100,
                0.500:21.300,
                0.750:26.700,
                1.000:33.400,
                1.250:42.200,
                1.500:48.300,
                2.000:60.300,
                2.500:73.000,
                3.000:88.900,
                3.500:101.600,
                4.000:114.300,
                5.000:141.300,
                6.000:168.300,
                8.000:219.100,
                10.000:273.000,
                12.000:323.800,
                14.000:355.600,
                16.000:406.400,
                18.000:457.000
              }
        return outside[float(self.line_number.pipe_size)]
    @property
    def get_design_thickness(self):
        # ( design_pressure * actual_outside_diameter)/((2*stress*joint_efficiency)+(2*design_pressure*0.4)) = (0.5*acual_outside_diameter)/(stess*joint_effiency/design_pressure+0.4)
        return (0.5*self.actual_outside_diameter)/(self.line_number.stress*self.line_number.joint_efficiency/self.line_number.design_pressure+0.4)
    
    @property
    def get_structural_thickness(self):
        if self.line_number.pipe_size <= 2:
            return 1.80
        elif self.line_number.pipe_size == 3:
            return 2.00
        elif self.line_number.pipe_size <= 4:
            return 2.30
        elif self.line_number.pipe_size <= 6 and self.line_number.pipe_size <=18:
            return 2.80
        elif self.line_number.pipe_size >=20:
            return 3.10
    @property
    def get_require_thickness(self):
        return max(self.design_thickness, self.structural_thickness)

    def save(self, *args, **kwarg):
        self.actual_outside_diameter = self.get_actual_outside
        self.design_thickness = self.get_design_thickness
        self.structural_thickness = self.get_structural_thickness
        self.require_thickness = self.get_require_thickness
        super(CML, self).save(*args, **kwarg)

    class Meta:
        verbose_name_plural = "Cml"

    def __str__(self):
        return "cn: " + str(self.cml_number) + " , ln: " + str(self.line_number.line_number)

class Test_Point(models.Model):
    cml_number = models.ForeignKey(CML, on_delete=models.CASCADE, default=None, verbose_name="Cml")
    tp_number = models.IntegerField()
    tp_description = models.IntegerField()
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Test_Point"

    def __str__(self):
        return "tn: " + str(self.tp_number) + " , " + str(self.cml_number)

class Thickness(models.Model):
    tp_number = models.ForeignKey(Test_Point, on_delete=models.CASCADE, default=None, verbose_name="Test_Point")
    inspection_date = models.DateField()
    actual_thickness = models.FloatField()

    def __str__(self):
        return str(self.tp_number) + " , " + str(self.inspection_date)
