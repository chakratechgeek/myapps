import json
import os
from django.http import JsonResponse, HttpResponseBadRequest, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import Software
from django.utils.dateparse import parse_datetime

def get_python_script(request):
    script_path = os.path.join(os.path.dirname(__file__), 'send_software.py')
    return FileResponse(open(script_path, 'rb'), content_type='text/x-python')


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

    software_objects = []
    for entry in data:
        try:
            software_objects.append(Software(
                hostname=entry.get('hostname'),
                software_name=entry.get('software_name'),
                version=entry.get('version'),
                license_key=entry.get('license_key', ''),
                is_valid=entry.get('is_valid', True),
                installed_at=parse_datetime(entry.get('installed_at')) if entry.get('installed_at') else None,
                last_used_at=parse_datetime(entry.get('last_used_at')) if entry.get('last_used_at') else None,
                is_active_user=entry.get('is_active_user', True),
            ))
        except Exception:
            continue  # optionally log the error

    Software.objects.bulk_create(software_objects)

    return JsonResponse({
        "message": "Software list collected",
        "count": len(software_objects)
    }, status=201)


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

    software = Software.objects.create(
        hostname=hostname,
        software_name=software_name,
        version=version,
        license_key=data.get('license_key', ''),
        is_valid=data.get('is_valid', True),
        installed_at=parse_datetime(data.get('installed_at')) if data.get('installed_at') else None,
        last_used_at=parse_datetime(data.get('last_used_at')) if data.get('last_used_at') else None,
        is_active_user=data.get('is_active_user', True),
    )

    return JsonResponse({
        "id": software.id,
        "hostname": software.hostname,
        "software_name": software.software_name,
        "version": software.version,
        "license_key": software.license_key,
        "is_valid": software.is_valid,
        "installed_at": software.installed_at,
        "last_used_at": software.last_used_at,
        "is_active_user": software.is_active_user
    }, status=201)


@require_GET
def list_software_api(request):
    qs = Software.objects.all().values(
        'id', 'hostname', 'software_name', 'version',
        'license_key', 'is_valid', 'installed_at',
        'last_used_at', 'is_active_user'
    )
    return JsonResponse(list(qs), safe=False)
