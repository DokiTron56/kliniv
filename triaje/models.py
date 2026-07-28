from django.db import models

class Sintoma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Recomendacion(models.Model):
    sintoma_relacionado = models.ForeignKey('Sintoma', on_delete=models.CASCADE)
    nivel_dolor_minimo = models.IntegerField(default=1)
    nivel_dolor_maximo = models.IntegerField(default=10)
    texto_recomendacion = models.TextField()
    medicamentos_sugeridos = models.CharField(max_length=200, help_text="Solo venta libre")
    
    # --- NUEVO CAMPO: PRECAUCIONES ---
    precauciones = models.TextField(
        blank=True, 
        default="", 
        help_text="Precauciones a considerar antes de seguir esta recomendación (Ej: Precaución en caso de embarazo o hipertensión)."
    )
    
    # --- CAMPO ADVERTENCIAS EXISTENTE ---
    advertencias = models.TextField(
        blank=True, 
        default="", 
        help_text="Advertencias de riesgo (Ej: Si el dolor persiste por más de 3 días, acuda a un médico)."
    )

    def __str__(self):
        return f"Recomendación para {self.sintoma_relacionado.nombre} (Dolor: {self.nivel_dolor_minimo}-{self.nivel_dolor_maximo})"

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

class MitoVerdad(models.Model):
    mito = models.CharField(max_length=200, help_text="Ej: Los antibióticos curan el resfriado.")
    verdad = models.CharField(max_length=200, help_text="Ej: Los resfriados son virales, no se tratan con antibióticos.")
    activo = models.BooleanField(default=True, help_text="Desmárcalo si quieres ocultarlo temporalmente de la página web.")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mito y Verdad"
        verbose_name_plural = "Mitos y Verdades"
        ordering = ['-fecha_creacion'] # Los más nuevos saldrán primero

    def __str__(self):
        return f"Mito: {self.mito}"

class MedicamentoOTC(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Paracetamol 500mg")
    para_que_sirve = models.CharField(max_length=200, help_text="Ej: Alivia el dolor leve a moderado y reduce la fiebre.")
    dosis_recomendada = models.CharField(max_length=200, help_text="Ej: 1 comprimido cada 8 horas (Máx. 4 al día).")
    
    # AQUÍ ESTÁ EL TRUCO: verbose_name cambia el título en el admin
    precauciones = models.TextField(
        verbose_name="Contraindicaciones",
        blank=True, 
        help_text="Ej: No usar en caso de daño hepático o consumo de alcohol."
    )
    
    activo = models.BooleanField(default=True, help_text="Desmárcalo para ocultarlo de la página.")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Medicamento OTC"
        verbose_name_plural = "Medicamentos OTC"
        ordering = ['nombre'] 

    def __str__(self):
        return self.nombre

class PagoArgolla(models.Model):
    PAGADOR_CHOICES = [
        ('Feli', 'Feli'),
        ('Any', 'Any'),
        ('Andreina', 'Andreina (Préstamo)'), # NUEVA OPCIÓN
    ]
    DESTINO_CHOICES = [
        ('Cecilia', 'Cecilia (Joyera)'),
        ('Andreina', 'Andreina (Mamá)'),
    ]
    
    quien_paga = models.CharField(max_length=15, choices=PAGADOR_CHOICES) # Cambié max_length a 15
    a_quien = models.CharField(max_length=15, choices=DESTINO_CHOICES)
    monto = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Pago de Argolla"
        verbose_name_plural = "Pagos de Argollas"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.quien_paga} pagó ${self.monto} a {self.a_quien}"