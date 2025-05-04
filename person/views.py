import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import Person

@csrf_exempt
def add_person_api(request):
    """
    Create a Person from either:
      • GET /person/api/add/?name=Alice&age=30
      • POST /person/api/add/  with JSON body {"name":"Alice","age":30}
    Returns JSON {id, name, age}.
    """
    # 1) Parse input
    if request.method == 'GET':
        name = request.GET.get('name')
        age  = request.GET.get('age')
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body)
            name = payload.get('name')
            age  = payload.get('age')
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        return JsonResponse({'error': 'Use GET or POST'}, status=405)

    # 2) Validate
    if not name or age is None:
        return HttpResponseBadRequest('Both name and age are required')
    try:
        age = int(age)
    except (ValueError, TypeError):
        return HttpResponseBadRequest('Age must be an integer')

    # 3) Persist
    person = Person.objects.create(name=name, age=age)

    # 4) Respond
    return JsonResponse({
        'id':   person.id,
        'name': person.name,
        'age':  person.age
    }, status=201)


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
    
@require_GET
def list_person_api(request):
    """
    GET /person/api/list/
    Returns JSON array of all persons: [{"id":1,"name":"Alice","age":30}, …]
    """
    # Query all people and serialize selected fields
    qs = Person.objects.all().values('id', 'name', 'age')
    # Convert QuerySet into a list of dicts
    persons = list(qs)
    return JsonResponse(persons, safe=False)