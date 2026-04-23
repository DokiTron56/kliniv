from django.db import models

class Sintoma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Recomendacion(models.Model):
    sintoma_relacionado = models.ForeignKey(Sintoma, on_delete=models.CASCADE)
    nivel_dolor_minimo = models.IntegerField(default=1)
    nivel_dolor_maximo = models.IntegerField(default=10)
    texto_recomendacion = models.TextField()
    medicamentos_sugeridos = models.CharField(max_length=200, help_text="Solo venta libre")

    def __str__(self):
        return f"Recomendación para {self.sintoma_relacionado.nombre}"

class Consulta(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    sintoma = models.ForeignKey(Sintoma, on_delete=models.SET_NULL, null=True)
    nivel_dolor = models.IntegerField()

    def __str__(self):
        return f"Consulta: {self.sintoma} - Dolor: {self.nivel_dolor}"

class Consejo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo