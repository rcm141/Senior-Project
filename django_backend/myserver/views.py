from django.http import HTTPResponse

def testPOST(request):
    if(request.method == 'POST'):
        return HTTPResponse(status=200)