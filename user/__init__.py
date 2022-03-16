from .apis import Registration, Login, LogOut, Home, AddNote, NotesOperation

routes_ = [
    (Registration, '/registration'),
    (Login, '/login'),
    (LogOut, '/logout'),
    (Home, '/'),
    (AddNote, '/addnote'),
    (NotesOperation, '/notes/<topic>')
]