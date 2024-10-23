import redis
import uuid
from typing import Callable, Optional
from functools import wraps

class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self):
        """Initialize the Cache with a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """Store data in Redis with a random key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """Get a value from Redis and convert it if a conversion function is provided.
        
        Args:
            key (str): The key to retrieve.
            fn (Optional[Callable]): A function to convert the data.

        Returns:
            The value stored in Redis, converted if fn is provided.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Get a string value from Redis.
        
        Args:
            key (str): The key to retrieve.

        Returns:
            str: The decoded value.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Get an integer value from Redis.
        
        Args:
            key (str): The key to retrieve.

        Returns:
            int: The integer value.
        """
        return self.get(key, int)

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """Decorator to count calls to a method in Redis.
        
        Args:
            method (Callable): The method to decorate.

        Returns:
            Callable: The wrapped function.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """Decorator to store the input/output history of a method.
        
        Args:
            method (Callable): The method to decorate.

        Returns:
            Callable: The wrapped function.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"
            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(result))
            return result
        return wrapper

    @call_history
    @count_calls
    def store(self, data):
        """Store data in Redis with a random key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

