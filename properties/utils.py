from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties from cache or database.
    Checks Redis for 'all_properties', fetches from database if not found,
    and stores in Redis for 1 hour (3600 seconds).
    """
    # Check Redis cache first
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, fetch from database
        properties = Property.objects.all()
        # Store in Redis cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties

