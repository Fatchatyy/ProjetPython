from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin qui vérifie si l'utilisateur est un administrateur.
    """
    def test_func(self):
        return self.request.user.is_superuser
