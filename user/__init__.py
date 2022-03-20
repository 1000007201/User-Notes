from .apis import Registration, Login, LogOut, ChangePass, Activate, ForgetPass, SetPass

user_routes = [
    (Registration, '/registration'),
    # (Registration_API, '/api/user/registration')
    (Login, '/login'),
    (LogOut, '/logout'),
    (ChangePass, '/changepass'),
    (Activate, '/activate'),
    (ForgetPass, '/forget'),
    (SetPass, '/setpass')
]
