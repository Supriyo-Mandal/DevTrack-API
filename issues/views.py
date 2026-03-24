import json
from pathlib import Path
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTERS_FILE = BASE_DIR / 'reporters.json'
ISSUES_FILE = BASE_DIR / 'issues.json'


def _read_data(file_path):
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@csrf_exempt
def reporters_view(request):
    if request.method == 'GET':
        reporters = _read_data(REPORTERS_FILE)
        reporter_id = request.GET.get('id')
        if reporter_id:
            try:
                rid = int(reporter_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid id'}, status=400)
            for rep in reporters:
                if rep['id'] == rid:
                    return JsonResponse(rep, status=200)
            return JsonResponse({'error': 'Reporter not found'}, status=404)
        return JsonResponse(reporters, safe=False, status=200)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        try:
            reporter = Reporter(data['id'], data.get('name', ''), data.get('email', ''), data.get('team', ''))
            reporter.validate()
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e.args[0]}'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        reporters = _read_data(REPORTERS_FILE)
        if any(rep['id'] == reporter.id for rep in reporters):
            return JsonResponse({'error': 'Reporter with this id already exists'}, status=400)

        reporters.append(reporter.to_dict())
        _write_data(REPORTERS_FILE, reporters)
        return JsonResponse(reporter.to_dict(), status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def issues_view(request):
    if request.method == 'GET':
        issues = _read_data(ISSUES_FILE)
        issue_id = request.GET.get('id')
        status_filter = request.GET.get('status')

        if issue_id:
            try:
                iid = int(issue_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid id'}, status=400)
            for issue in issues:
                if issue['id'] == iid:
                    return JsonResponse(issue, status=200)
            return JsonResponse({'error': 'Issue not found'}, status=404)

        if status_filter:
            filtered = [issue for issue in issues if issue['status'] == status_filter]
            return JsonResponse(filtered, safe=False, status=200)

        return JsonResponse(issues, safe=False, status=200)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        try:
            priority = data.get('priority')
            if priority == 'critical':
                issue = CriticalIssue(data['id'], data.get('title', ''), data.get('description', ''), data.get('status', ''), priority, data['reporter_id'])
            elif priority == 'low':
                issue = LowPriorityIssue(data['id'], data.get('title', ''), data.get('description', ''), data.get('status', ''), priority, data['reporter_id'])
            else:
                issue = Issue(data['id'], data.get('title', ''), data.get('description', ''), data.get('status', ''), priority, data['reporter_id'])
            issue.validate()
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e.args[0]}'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        issues = _read_data(ISSUES_FILE)
        if any(i['id'] == issue.id for i in issues):
            return JsonResponse({'error': 'Issue with this id already exists'}, status=400)

        # Ensure reporter exists
        reporters = _read_data(REPORTERS_FILE)
        if not any(r['id'] == issue.reporter_id for r in reporters):
            return JsonResponse({'error': 'Reporter not found'}, status=404)

        entry = issue.to_dict()
        entry['message'] = issue.describe()

        issues.append(entry)
        _write_data(ISSUES_FILE, issues)

        return JsonResponse(entry, status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])
