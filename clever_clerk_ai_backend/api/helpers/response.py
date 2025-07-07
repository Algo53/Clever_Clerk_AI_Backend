def api_response(data=None, success=True, successText=None, errorText=None):
    return {
        "data": data,
        "success": success,
        "successText": successText,
        "errorText": errorText,
    }
