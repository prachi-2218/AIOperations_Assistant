import hashlib
import json
import time
from typing import Any, Optional, Dict

class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key based on function name and arguments"""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, func_name: str, args: tuple, kwargs: dict) -> Optional[Any]:
        """Get cached value if exists and not expired"""
        key = self._generate_key(func_name, args, kwargs)
        
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl_seconds:
                print(f"Cache hit for {func_name}")
                return entry['value']
            else:
                # Remove expired entry
                del self.cache[key]
        
        return None
    
    def set(self, func_name: str, args: tuple, kwargs: dict, value: Any) -> None:
        """Set value in cache"""
        key = self._generate_key(func_name, args, kwargs)
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        print(f"Cached result for {func_name}")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        print("Cache cleared")
    
    def size(self) -> int:
        """Get number of cached entries"""
        return len(self.cache)

# Global cache instance
cache = SimpleCache(ttl_seconds=300)  # 5 minutes

def cached_function(ttl_seconds: int = 300):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Try to get from cache first
            cached_result = cache.get(func.__name__, args, kwargs)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(func.__name__, args, kwargs, result)
            return result
        
        return wrapper
    return decorator
