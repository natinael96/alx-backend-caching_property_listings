import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Connects to Redis via django_redis, gets keyspace statistics,
    calculates hit ratio, logs metrics, and returns a dictionary.
    """
    try:
        # Connect to Redis via django_redis
        redis_conn = get_redis_connection("default")
        
        # Get INFO command output
        info = redis_conn.info('stats')
        
        # Extract keyspace_hits and keyspace_misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': hit_ratio,
        }
        
        # Log metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, "
            f"Misses: {keyspace_misses}, "
            f"Total: {total_requests}, "
            f"Hit Ratio: {hit_ratio:.2%}"
        )
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }

