from django.db import models

# Create your models here.
class Fotos_portada(models.Model):
    podium = models.TextField(max_length = 1000000, default = 'NC')
    historico = models.TextField(max_length = 1000000, default = 'NC')
    descenso = models.TextField(max_length = 1000000, default = 'NC')

class Titulos(models.Model):
    nombre = models.CharField(max_length=25)
    titulos = models.IntegerField(default = 0)
    

    class Meta:
        verbose_name = 'Titulos'
        verbose_name_plural = 'Titulos'
    def __str__(self):
        return self.nombre

class Historico(models.Model):
    nombre = models.CharField(max_length=100)
    Q1 = models.IntegerField(default=0)
    Q2 = models.IntegerField(default=0)
    Q3 = models.IntegerField(default=0)
    Q4 = models.IntegerField(default=0)
    Q5 = models.IntegerField(default=0)
    Q6 = models.IntegerField(default=0)
    Q7 = models.IntegerField(default=0)
    Q8 = models.IntegerField(default=0)
    Q9 = models.IntegerField(default=0)
    Q10 = models.IntegerField(default=0)
    Q11 = models.IntegerField(default=0)
    Q12 = models.IntegerField(default=0)
    Q13 = models.IntegerField(default=0)
    Q14 = models.IntegerField(default=0)
    Q15 = models.IntegerField(default=0)
    Q16 = models.IntegerField(default=0)
    Q17 = models.IntegerField(default=0)
    Q18 = models.IntegerField(default=0)
    Q19 = models.IntegerField(default=0)
    Q20 = models.IntegerField(default=0)
    Q21 = models.IntegerField(default=0)
    Q22 = models.IntegerField(default=0)
    Q23 = models.IntegerField(default=0)
    Q24 = models.IntegerField(default=0)
    Q25 = models.IntegerField(default=0)
    Q26 = models.IntegerField(default=0)
    Q27 = models.IntegerField(default=0)
    Q28 = models.IntegerField(default=0)
    Q29 = models.IntegerField(default=0)
    Q30 = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Historico'
        verbose_name_plural = 'Historicos'
    def __str__(self):
        return self.nombre