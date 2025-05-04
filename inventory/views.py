import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import Software
from django.http import FileResponse
import os

def get_powershell_script(request):
    script_path = os.path.join(os.path.dirname(__file__), 'send-software.ps1')
    return FileResponse(open(script_path, 'rb'), content_type='text/plain')

@csrf_exempt
def collect_software_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not isinstance(data, list):
        return HttpResponseBadRequest("Expected a list of software records")

    for entry in data:
        Software.objects.create(
            hostname=entry.get('hostname'),
            software_name=entry.get('software_name'),
            version=entry.get('version'),
            license_key=entry.get('license_key', ''),
            is_valid=entry.get('is_valid', True)
        )

    return JsonResponse({"message": "Software list collected", "count": len(data)}, status=201)


@csrf_exempt
def add_software_api(request):
    if request.method == 'GET':
        data = request.GET
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        return JsonResponse({'error': 'Use GET or POST'}, status=405)

    hostname = data.get('hostname')
    software_name = data.get('software_name')
    version = data.get('version')

    if not all([hostname, software_name, version]):
        return HttpResponseBadRequest("hostname, software_name, and version are required.")

    license_key = data.get('license_key')
    is_valid = data.get('is_valid', True)

    software = Software.objects.create(
        hostname=hostname,
        software_name=software_name,
        version=version,
        license_key=license_key,
        is_valid=is_valid
    )

    return JsonResponse({
        "id": software.id,
        "hostname": software.hostname,
        "software_name": software.software_name,
        "version": software.version,
        "license_key": software.license_key,
        "is_valid": software.is_valid,
        "installed_at": software.installed_at
    }, status=201)


@require_GET
def list_software_api(request):
    qs = Software.objects.all().values(
        'id', 'hostname', 'software_name', 'version',
        'license_key', 'is_valid', 'installed_at'
    )
    return JsonResponse(list(qs), safe=False)
