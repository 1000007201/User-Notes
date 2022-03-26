from .apis import AddNote, NotesOperation, Home, NoteLabel, GetByLabel

notes_routes = [
    (AddNote, '/addnotes'),
    (NotesOperation, '/notes/<topic>'),
    (NoteLabel, '/api/label/<id>'),
    (GetByLabel, '/api/getbylabel/<label>'),
    (Home, '/')
]
