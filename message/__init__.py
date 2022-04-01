from .apis import SendMessage, CheckMessage, GiveAccess, MessageNote

message_routes = [
    (SendMessage, '/api/send/message'),
    (CheckMessage, '/api/check/message'),
    (GiveAccess, '/api/give/access/<msg_id>'),
    (MessageNote, '/api/update/message/note/<msg_id>')
]
