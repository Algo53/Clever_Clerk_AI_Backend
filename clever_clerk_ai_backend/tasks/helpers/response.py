# api/helpers/response.py
from rest_framework.response import Response

def api_response(*, success: bool, successText: str = None, errorText: str = None, data=None, status_code=200):
    payload = {
        "success": success,
        "successText": successText if success else None,
        "errorText": errorText if not success else None,
        "data": data
    }
    return Response(payload, status=status_code)
