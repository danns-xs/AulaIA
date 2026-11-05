
import os
from pathlib import Path

from django.shortcuts import render
from dotenv import load_dotenv
from google import genai

# Cargar las variables del archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def inicio(request):
    return render(request, 'core/inicio.html')


def modulo(request, seccion):

    contenidos = {
        'aprende': {
            'titulo': 'Aprende sobre inteligencia artificial',
            'descripcion': 'Descubre qué es la IA, cómo funciona y cuáles son sus principales aplicaciones.',
            'temas': [
                '¿Qué es la inteligencia artificial?',
                'Tipos de inteligencia artificial',
                'Aplicaciones en la vida cotidiana',
                'Ventajas y limitaciones'
            ]
        },

        'prompts': {
            'titulo': 'Aprende a utilizar la IA',
            'descripcion': 'Conoce cómo comunicarte con las herramientas de inteligencia artificial.',
            'temas': [
                '¿Qué es un prompt?',
                'Cómo formular instrucciones claras',
                'Ejemplos de buenos prompts',
                'Errores frecuentes al utilizar IA'
            ]
        },

        'responsable': {
            'titulo': 'Uso responsable de la IA',
            'descripcion': 'Aprende a utilizar estas herramientas de forma crítica, segura y consciente.',
            'temas': [
                'Protección de datos personales',
                'Verificación de información',
                'Sesgos y limitaciones',
                'Pensamiento crítico y autonomía'
            ]
        },

        'actividades': {
            'titulo': 'Pon a prueba tus conocimientos',
            'descripcion': 'Refuerza lo aprendido mediante actividades y cuestionarios.',
            'temas': [
                'Cuestionarios de conocimientos',
                'Retos de aprendizaje',
                'Retroalimentación de respuestas'
            ]
        },

        'asistente': {
            'titulo': 'Tu asistente de inteligencia artificial',
            'descripcion': 'Un espacio para resolver dudas y aprender a utilizar estas herramientas.',
            'temas': []
        }
    }

    contenido = contenidos.get(seccion)

    if not contenido:
        return render(request, 'core/inicio.html')

    respuesta = None
    error = None

    # Procesamiento del asistente AulaIA
    if seccion == 'asistente' and request.method == 'POST':

        pregunta = request.POST.get('pregunta', '').strip()

        if not pregunta:
            error = 'Escribe una pregunta para continuar.'

        elif len(pregunta) > 1000:
            error = 'Tu pregunta es demasiado larga. Intenta resumirla.'

        else:
            api_key = os.getenv('GEMINI_API_KEY')

            if not api_key:
                error = 'El asistente todavía no está configurado.'

            else:
                try:
                    with genai.Client(api_key=api_key) as client:

                        resultado = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=pregunta,
                            config={
                                'system_instruction': (
                                    'Eres el asistente educativo de AulaIA. '
                                    'Tu objetivo es explicar la inteligencia artificial '
                                    'de manera clara, sencilla y responsable. '
                                    'Promueve el pensamiento crítico, la verificación '
                                    'de información y la protección de datos personales. '
                                    'Responde en español y con lenguaje respetuoso. '
                                    'Si te preguntan sobre otro tema, responde brevemente '
                                    'y orienta la conversación hacia la educación y la IA.'
                                ),
                                'max_output_tokens': 500
                            }
                        )

                        respuesta = resultado.text

                        if not respuesta:
                            error = 'El asistente no generó una respuesta. Inténtalo nuevamente.'

                except Exception as e:
                    print("ERROR DE GEMINI:", type(e).__name__, str(e))
                    error = 'No fue posible obtener una respuesta. Revisa la terminal para identificar el problema.'

    return render(request, 'core/modulo.html', {
        'contenido': contenido,
        'seccion': seccion,
        'respuesta': respuesta,
        'error': error
    })
