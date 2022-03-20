from .apis import AddNote, NotesOperation, Home, AddLabel, GetByLabel

notes_routes = [
    (AddNote, '/addnotes'),
    (NotesOperation, '/notes/<topic>'),
    (AddLabel, '/api/label/<id>'),
    (GetByLabel, '/api/getbylabel/<label>'),
    (Home, '/')
]
