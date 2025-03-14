from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

 # Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

 # Importe requests y json
import requests
import json
from collections import Counter
from datetime import datetime

@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
        
     # Arme el endpoint del REST API
     current_url = request.build_absolute_uri()
     url = current_url + '/api/v1/landing'

     # Petición al REST API
     response_http = requests.get(url)
     response_dict = json.loads(response_http.content)

     print("Endpoint ", url)
     print("Response ", response_dict)

     # Respuestas totales
     total_responses = len(response_dict.keys())

     # Valores de la respuesta
     responses = response_dict.values()

     

     # Objeto con los datos a renderizar
     data = {
         'title': 'Landing - Dashboard',
         'total_responses': total_responses,
         'responses': responses
     }

     

     # Renderización en la plantilla
     return render(request, 'main/index.html', data)
