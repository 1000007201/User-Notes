from .apis import Registration, Login, LogOut, ChangePass, ForgetPass, SetPass, ActivateView

user_routes = [
    (Registration, '/registration'),
    # (Registration_API, '/api/user/registration')
    (Login, '/login'),
    (LogOut, '/logout'),
    (ChangePass, '/changepass'),
    # (ActivateView, '/activate'),
    (ForgetPass, '/forget'),
    (SetPass, '/setpass')
]
