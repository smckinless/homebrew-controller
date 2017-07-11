from rest_framework.views import APIView
from rest_framework.response import Response

class TempData(APIView):

    def get(self, request):
        print 'hey'
        return Response([])

    def post(self, request):
        print request.data
        return Response([])