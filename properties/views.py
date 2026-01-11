from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property


@cache_page(60 * 15)
def property_list(request):
    """Return all properties as JSON response, cached for 15 minutes."""
    properties = Property.objects.all()
    properties_data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        }
        for prop in properties
    ]
    return JsonResponse({'properties': properties_data}, safe=False)

