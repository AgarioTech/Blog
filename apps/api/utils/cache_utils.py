from django.core.cache import cache
from django_redis import get_redis_connection

from apps.api.services.others import clear_cache

redis_client = get_redis_connection()

class CacheAndClearMixin:

    cache_prefix = ''

    def clear_cache(self):

        keys = cache.get(f'{self.cache_prefix}_cache_keys') or set()

        for key in keys:
            cache.delete(key)
        cache.delete(f'{self.cache_prefix}_cache_keys')

    def get_cached_data(self, request,
                        prefix,
                        queryset,
                        page,
                        serializer_class,
                        paginated_response):
        self.cache_prefix = prefix
        cache_key = f'{self.cache_prefix}{request.get_full_path().replace('/', '_')
        .replace('?', '_')
        .replace('&', '_')
        .replace('=', '_')}'

        keys = cache.get(f'{self.cache_prefix}_cache_keys') or set()
        keys.add(cache_key)
        cache.set(f'{self.cache_prefix}_cache_keys', keys, None)
        data = cache.get(cache_key)
        if data:
            return data

        if page is not None:
            serializer = serializer_class(instance=page, many=True, context={'request': request})
            data = paginated_response(serializer.data).data
        else:
            serializer = serializer_class(instance=queryset, many=True, context={'request': request})
            data = serializer.data
        cache.set(cache_key, data, None)
        return data

    def perform_update(self, serializer):
        self.clear_cache()
        serializer.save()

    def perform_destroy(self, instance):
        self.clear_cache()
        instance.delete()

    def perform_create(self, serializer):
        self.clear_cache()
        serializer.save()