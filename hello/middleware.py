from django.urls import reverse
from django.shortcuts import redirect

class ProfileCompletitionMiddleware:
    """
    Ensure every user that is interacting with the platform
    have their profile picture and biography
    """
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        if not request.user.is_anonymous and not request.user.is_staff:
            print(request.path)
            profile = request.user.profile
            if not profile.picture or not profile.biography:
                if request.path not in [reverse('users:update'), reverse('users:logout')]:
                    return redirect('users:update')

        response = self.get_response(request)
        return response
