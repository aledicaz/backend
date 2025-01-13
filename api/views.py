from django.shortcuts import render

# Create your views here.
 # Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
     name = 'Landing API'

     # Coloque el nombre de su colección en el Realtime Database
     collection_name = 'emails'

     def get(self, request):

         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')
		    
         # get: Obtiene todos los elementos de la colección
         data = ref.get()

         # Devuelve un arreglo JSON
         return Response(data, status=status.HTTP_200_OK)
     
     def post(self, request):
	        
         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')

         current_time  = datetime.now()
         custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
         request.data.update({"saved": custom_format })
	        
         # push: Guarda el objeto en la colección
         new_resource = ref.push(request.data)
	        
         # Devuelve el id del objeto guardado
         return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
     
class LandingAPIDetail(APIView):

    name = 'Landing Detail API'

    collection_name = 'emails'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        documento = dict(ref.get()).get(pk)
        print(documento)

        if documento:
            return Response(documento, status=status.HTTP_200_OK)
        return Response({'error': 'Documento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        documento = ref.get().get(pk)

        if not documento:
            return Response({'error': 'Documento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if 'email' not in request.data:
            return Response(
                {'error': 'La petición no incluye el campo requerido "email"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar los campos existentes en el documento
        documento.update(request.data)
        ref.child(pk).set(documento)

        return Response({'message': 'Documento actualizado exitosamente'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        documento = ref.get().get(pk)

        if not documento:
            return Response({'error': 'Documento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        ref.child(pk).delete()
        return Response({'message': 'Documento eliminado exitosamente'}, status=status.HTTP_200_OK)