from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from .models import User 

class ProfileViewCounterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and resolve(request.path_info).url_name == 'view_profile':
            user_profile = view_kwargs.get('slug')
            if user_profile and user_profile != request.user.slug:
                user = User.objects.get(slug=user_profile)
                user.profile_views += 1
                user.save()
        return None
