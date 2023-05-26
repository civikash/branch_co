from django.http import JsonResponse
from reports.models import InfEconOp, SecondInfEconOp

def delete_marfa(request, code):
    try:
        # Найти объект по коду и удалить его из базы данных
        marfa = SecondInfEconOp.objects.get(code=code)
        marfa.delete()
        return JsonResponse({'success': True})
    except SecondInfEconOp.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Строка не найдена'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})