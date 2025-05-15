from django.http import JsonResponse
from django.views import View
import time
import random
import string
from django.core.cache import cache

# Bearer token to authenticate
BEARER_TOKEN = "mf8nrqICaHYD1y8wRMBksWm7U7gLgXy1mSWjhI0q"

class APIViewWithDDOSProtection(View):

    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _check_and_update_rate_limit(self, client_ip):
        """Check and update rate limit for the IP"""
        current_time = time.time()

        # Temporary block key (20 minutes)
        if cache.get(f'block_temporary:{client_ip}'):
            return False, "Temporary block: Too many requests in a short time."

        rate_limit_key = f'rate_limit:{client_ip}'
        attempts = cache.get(rate_limit_key, [])

        # Remove requests older than 20 seconds
        attempts = [timestamp for timestamp in attempts if current_time - timestamp < 20]
        attempts.append(current_time)

        # Store the updated attempt list in the cache
        cache.set(rate_limit_key, attempts, timeout=60)

        # If more than 10 requests in 20 seconds, block temporarily
        if len(attempts) > 10:
            cache.set(f'block_temporary:{client_ip}', True, timeout=1200)  # 20 minutes
            return False, "Temporary block: Too many requests in a short time."

        # If more than 100 requests in 1 minute, block permanently
        if len(attempts) > 100:
            cache.set(f'permanent_block:{client_ip}', True, timeout=None)
            return False, "Permanent block: Too many violations."

        return True, None

    def dispatch(self, request, *args, **kwargs):
        """Intercept requests to handle rate-limiting and authentication"""
        client_ip = self._get_client_ip(request)

        # Check rate-limiting before continuing
        is_allowed, error_message = self._check_and_update_rate_limit(client_ip)
        if not is_allowed:
            return JsonResponse({"error": error_message}, status=400)

        # Check the Authorization header for the Bearer token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Missing or invalid authentication token"}, status=400)

        token = auth_header.split(" ")[1]
        if token != BEARER_TOKEN:
            return JsonResponse({"error": "Invalid bearer token"}, status=400)

        # Return random JSON data on successful authentication
        mock_data = {
            "name": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            "email": ''.join(random.choices(string.ascii_lowercase, k=5)) + "@example.com",
            "address": ''.join(random.choices(string.ascii_lowercase + string.digits, k=15)),
            "phone_number": ''.join(random.choices(string.digits, k=10))
        }

        return JsonResponse(mock_data, status=200)
