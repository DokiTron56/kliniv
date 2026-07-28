from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Sintoma, Recomendacion, Consulta, Consejo, MitoVerdad, MedicamentoOTC, PagoArgolla

def inicio(request):
    # Traemos TODOS los datos necesarios para la página principal
    lista_consejos = Consejo.objects.all().order_by('-fecha_publicacion')
    total_consultas = Consulta.objects.count()
    sintomas_frecuentes = Consulta.objects.values('sintoma__nombre').annotate(total=Count('id')).order_by('-total')
    
    contexto = {
        'consejos': lista_consejos,
        'total_consultas': total_consultas,
        'sintomas_frecuentes': sintomas_frecuentes
    }
    return render(request, 'index.html', contexto)

def evaluacion(request):
    sintomas_disponibles = Sintoma.objects.all()
    return render(request, 'evaluacion.html', {'sintomas': sintomas_disponibles})

def procesar_evaluacion(request):
    if request.method == 'POST':
        sintoma_id = request.POST.get('sintoma')
        nivel_dolor = int(request.POST.get('dolor'))
        
        sintoma_elegido = Sintoma.objects.get(id=sintoma_id)
        Consulta.objects.create(sintoma=sintoma_elegido, nivel_dolor=nivel_dolor)
        
        recomendacion = Recomendacion.objects.filter(
            sintoma_relacionado=sintoma_elegido,
            nivel_dolor_minimo__lte=nivel_dolor,
            nivel_dolor_maximo__gte=nivel_dolor
        ).first()
        
        contexto = {
            'sintoma': sintoma_elegido,
            'dolor': nivel_dolor,
            'recomendacion': recomendacion
        }
        return render(request, 'resultado.html', contexto)
    return redirect('inicio')

def sorpresa_any(request):
    return render(request, 'any.html')

# ==========================================
# NUEVAS VISTAS: GUÍA DE BIENESTAR
# ==========================================

def habitos(request):
    return render(request, 'habitos.html')

def mitos(request):
    # Aquí es donde ahora enviamos los mitos activos a su propia página
    mitos_activos = MitoVerdad.objects.filter(activo=True)
    return render(request, 'mitos.html', {'mitos': mitos_activos})

def calendario(request):
    return render(request, 'calendario.html')

def botiquin(request):
    return render(request, 'botiquin.html')

# (Asegúrate de importar MedicamentoOTC arriba junto a MitoVerdad)

def medicamentos_otc(request):
    lista_medicamentos = MedicamentoOTC.objects.filter(activo=True)
    return render(request, 'medicamentos_otc.html', {'medicamentos': lista_medicamentos})


def argollas(request):
    # 1. Si el formulario envía un nuevo pago, lo guardamos
    if request.method == 'POST':
        quien_paga = request.POST.get('quien_paga')
        a_quien = request.POST.get('a_quien')
        monto = int(request.POST.get('monto', 0))
        
        if quien_paga and a_quien and monto > 0:
            PagoArgolla.objects.create(
                quien_paga=quien_paga,
                a_quien=a_quien,
                monto=monto,
                nota="Abono desde la web"
            )
        return redirect('argollas') # Recargamos la página limpia

    # 2. Valores Base Iniciales (Julio 2026)
    deuda_cecilia = 536000
    deuda_andreina = 73000
    aporte_feli = 46000
    aporte_any = 35000

    # 3. Sumar y restar según la base de datos
    pagos = PagoArgolla.objects.all()
    for pago in pagos:
        # A quién se le abonó el dinero (la deuda baja)
        if pago.a_quien == 'Cecilia':
            deuda_cecilia = max(0, deuda_cecilia - pago.monto)
        elif pago.a_quien == 'Andreina':
            deuda_andreina = max(0, deuda_andreina - pago.monto)
        
        # De dónde salió el dinero
        if pago.quien_paga == 'Feli':
            aporte_feli += pago.monto
        elif pago.quien_paga == 'Any':
            aporte_any += pago.monto
        elif pago.quien_paga == 'Andreina':
            # Si mamá sacó de su bolsillo, nuestra deuda con ella sube
            deuda_andreina += pago.monto

    # 4. Formatear para que se vea como dinero (ej: 536.000)
    context = {
        'deuda_cecilia': f"{deuda_cecilia:,}".replace(',', '.'),
        'deuda_andreina': f"{deuda_andreina:,}".replace(',', '.'),
        'aporte_feli': f"{aporte_feli:,}".replace(',', '.'),
        'aporte_any': f"{aporte_any:,}".replace(',', '.'),
        'pagos': pagos,
    }
    
    return render(request, 'argollas.html', context)