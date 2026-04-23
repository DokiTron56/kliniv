from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Sintoma, Recomendacion, Consulta, Consejo

def inicio(request):
    # Traemos TODOS los datos necesarios para la gran página principal
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