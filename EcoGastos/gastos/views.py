# gastos/views.py
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd

# Función reutilizable para convertir a float
def a_float(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0.0

# Páginas informativas
def inicio(request):
    return render(request, 'principal.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def asesoria(request):
    return render(request, 'asesoria.html')

def comparativas(request):
    return render(request, 'comparativas.html')

# Vista mensual
def gastos_mensuales(request):
    context = {}
    if request.method == 'POST':
        datos = {}
        campos = [
            'salario_neto', 'otros_ingresos',
            'alquiler_hipoteca', 'prestamos', 'impuestos',
            'agua', 'gas', 'luz', 'alimentacion', 'internet', 'transporte', 'educacion', 'imprevistos',
            'ocio', 'viajes', 'suscripciones', 'otros_gastos',
            'ahorro',
        ]

        for campo in campos:
            datos[campo] = a_float(request.POST.get(campo))

        # 2) Suma ingresos
        total_ingresos = datos['salario_neto'] + datos['otros_ingresos']

        # 3) Suma gastos
        gastos_oblig = (
            datos['alquiler_hipoteca']
            + datos['prestamos']
            + datos['impuestos']
        )
        gastos_deduc = (
            datos['agua']
            + datos['gas']
            + datos['luz']
            + datos['alimentacion']
            + datos['internet']
            + datos['transporte']
            + datos['educacion']
            + datos['imprevistos']
        )
        gastos_var = (
            datos['ocio']
            + datos['viajes']
            + datos['suscripciones']
            + datos['otros_gastos']
            + datos['ahorro']
        )

        total_gastos = gastos_oblig + gastos_deduc + gastos_var
        sobrante = total_ingresos - total_gastos

        context = {
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'sobrante': sobrante,
            **datos,
        }

    return render(request, 'mensuales.html', context)


# Exportación mensual
def exportar_excel(request):
    salario_neto = a_float(request.POST.get('salario_neto'))
    otros_ingresos = a_float(request.POST.get('otros_ingresos'))
    alquiler_hipoteca   = a_float(request.POST.get('alquiler_hipoteca'))
    prestamos   = a_float(request.POST.get('prestamos'))
    impuestos   = a_float(request.POST.get('impuestos'))
    agua        = a_float(request.POST.get('agua'))
    gas         = a_float(request.POST.get('gas'))
    luz         = a_float(request.POST.get('luz'))
    alimentacion = a_float(request.POST.get('alimentacion'))
    internet    = a_float(request.POST.get('internet'))
    transporte  = a_float(request.POST.get('transporte'))
    educacion   = a_float(request.POST.get('educacion'))
    imprevistos = a_float(request.POST.get('imprevistos'))
    ocio        = a_float(request.POST.get('ocio'))  
    viajes      = a_float(request.POST.get('viajes'))
    suscripciones = a_float(request.POST.get('suscripciones'))
    otros_gastos  = a_float(request.POST.get('otros_gastos'))
    ahorro      = a_float(request.POST.get('ahorro'))

    total_ingresos = (salario_neto + otros_ingresos)
    total_gastos = alquiler_hipoteca+ prestamos + impuestos + agua + gas + luz + alimentacion + internet + transporte + educacion + imprevistos + viajes + suscripciones + ocio + otros_gastos + ahorro
    deducibles   = alquiler_hipoteca+ impuestos + internet
    sobrante     = total_ingresos - total_gastos


    df = pd.DataFrame({
        'Concepto': [
            'Ingresos totales', 'alquiler_hipoteca', 'prestamos', 'Impuestos', 'Agua', 'Gas', 'Luz', 'Alimentacion', 'Internet', 'Transporte', 'Educacion', 'Imprevistos',
            'Ocio', 'viajes', 'Suscripciones', 'Otros_gastos',
            'ahorro', 'total_gastos', 'deducibles', 'sobrante'
        ],
        'Monto ($)': [
            total_ingresos, alquiler_hipoteca, prestamos, impuestos, agua, gas, luz, alimentacion, internet, transporte, educacion, imprevistos,
            ocio, viajes, suscripciones, otros_gastos,
            ahorro, total_gastos, deducibles, sobrante
        ]
    })

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="gastos_calculados.xlsx"'
    df.to_excel(response, index=False) 
    return response

#----------------------------------ANUALES------------------------------------------------------------------------------------------------------------------
# Vista anual
def gastos_anuales(request):
    context = {}
    if request.method == 'POST':
        def a_float(valor):
            try:
                return float(valor)
            except (ValueError, TypeError):
                return 0.0

        campos = [
            'salario_neto', 'otros_ingresos',
            'alquiler_hipoteca', 'prestamos', 'impuestos',
            'agua', 'gas', 'luz', 'alimentacion', 'internet', 'transporte', 'educacion',
            'imprevistos', 'ocio', 'viajes', 'suscripciones', 'otros_gastos' 
        ]

        datos = {campo: a_float(request.POST.get(campo)) for campo in campos}

        # Total ingresos anuales
        total_ingresos = (datos['salario_neto'] + datos['otros_ingresos']) * 12

        # Total gastos anuales
        gastos_oblig = (
            datos['alquiler_hipoteca'] + datos['prestamos'] + datos['impuestos']
        )

        gastos_deduc = (
            datos['agua'] + datos['gas'] + datos['luz'] + datos['alimentacion'] +
            datos['internet'] + datos['transporte'] +  datos['educacion'] + 
            datos['imprevistos']
        )

        gastos_var = (
            datos['ocio'] + datos['viajes'] +
            datos['suscripciones'] + datos['otros_gastos']
        )

        total_gastos = (gastos_oblig + gastos_deduc + gastos_var) * 12
        sobrante = total_ingresos - total_gastos

        # Pasar los valores al contexto
        context = {
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'sobrante': sobrante,
            **datos
        }

    return render(request, 'anuales.html', context)

# Exportación anual
def exportar_excel_anual(request):
    POST = request.POST

    salario_neto      = a_float(POST.get('salario_neto'))
    otros_ingresos    = a_float(POST.get('otros_ingresos'))
    alquiler_hipoteca = a_float(POST.get('alquiler_hipoteca'))
    prestamos         = a_float(POST.get('prestamos'))
    impuestos         = a_float(POST.get('impuestos'))
    agua              = a_float(POST.get('agua'))
    gas               = a_float(POST.get('gas'))
    luz               = a_float(POST.get('luz'))
    alimentacion      = a_float(POST.get('alimentacion'))
    internet          = a_float(POST.get('internet'))
    transporte        = a_float(POST.get('transporte'))
    educacion         = a_float(POST.get('educacion'))
    imprevistos       = a_float(POST.get('imprevistos'))
    ocio              = a_float(POST.get('ocio'))
    viajes            = a_float(POST.get('viajes'))
    suscripciones     = a_float(POST.get('suscripciones'))
    otros_gastos      = a_float(POST.get('otros_gastos'))

    multiplicador = 12

    total_ingresos = (salario_neto + otros_ingresos) * multiplicador
    gastos_oblig = (alquiler_hipoteca + prestamos + impuestos) * multiplicador
    gastos_deduc = (agua + gas + luz + alimentacion + internet + transporte + educacion + imprevistos) * multiplicador
    gastos_var = (ocio + viajes + suscripciones + otros_gastos) * multiplicador
    total_gastos = gastos_oblig + gastos_deduc + gastos_var
    sobrante = total_ingresos - total_gastos

    df = pd.DataFrame({
        'Concepto': [
            'Ingresos Totales', 'alquiler_hipoteca', 'prestamos', 'impuestos',
            'agua', 'gas', 'luz', 'alimentacion', 'internet', 'transporte', 'educacion',
            'imprevistos', 'ocio', 'viajes', 'suscripciones', 'otros_gastos', 'Gastos Obligatorios', 'Gastos Deducibles', 'Gastos Variables',
            'Total Gastos', 'Sobrante'
        ],
        'Monto ($)': [
            total_ingresos, alquiler_hipoteca, prestamos, impuestos,
            agua, gas, luz, alimentacion, internet, transporte, educacion,
            imprevistos, ocio, viajes, suscripciones, otros_gastos, gastos_oblig, gastos_deduc, gastos_var,
            total_gastos, sobrante
        ]
    })

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="gastos_anuales.xlsx"'
    df.to_excel(response, index=False)
    return response


def asesoria_view(request):
    enviado = False

    if request.method == 'POST':
        # Aquí puedes acceder a los datos si los necesitas
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        motivo = request.POST.get('motivo')
        enviado = True

    return render(request, 'asesoria.html', {'enviado': enviado})
