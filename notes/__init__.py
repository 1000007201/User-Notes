from .apis import AddNote, NotesOperation, Home, NoteLabel, GetByLabel, PinNote, UnpinNote, NoteAddTrash, NoteRemoveTrash

notes_routes = [
    (AddNote, '/addnotes'),
    (NotesOperation, '/notes/<note_id>'),
    (NoteLabel, '/api/label/<note_id>'),
    (GetByLabel, '/api/getbylabel/<label>'),
    (PinNote, '/api/pin/note/<note_id>'),
    (UnpinNote, '/api/unpin/note/<note_id>'),
    (NoteAddTrash, '/api/addtrash/note/<note_id>'),
    (NoteRemoveTrash, '/api/remtrash/note/<note_id>'),
    (Home, '/')
]
