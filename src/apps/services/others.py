from django.core.cache import cache

from apps.posts.models import Post
from apps.comments.models import Comment
from apps.users.models import Notifications, Subscription, CustomUser



def get_cached_data(request, prefix, queryset, page, serializer_class, paginated_response):
    cache_key = f'{prefix}{request.get_full_path().replace('/', '_')
                .replace('?', '_')
                .replace('&', '_')
                .replace('=', '_')}'

    keys = cache.get(f'{prefix}_cache_keys') or set()
    keys.add(cache_key)
    cache.set(f'{prefix}_cache_keys', keys, None)
    data = cache.get(cache_key)
    if data:
        print(cache_key)
        return data

    if page is not None:
        serializer = serializer_class(instance=page, many=True, context={'request': request})
        data = paginated_response(serializer.data).data
    else:
        serializer = serializer_class(instance=queryset, many=True, context={'request': request})
        data = serializer.data
    cache.set(cache_key, data, 60 * 2)
    return data


def clear_cache(prefix):
    keys = cache.get(f'{prefix}_cache_keys') or set()
    for key in keys:
        cache.delete(key)
    cache.delete(f'{prefix}_cache_keys')
