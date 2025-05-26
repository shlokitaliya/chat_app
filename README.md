# chat_app
| Page                  | URL             | Description                        |
| --------------------- | --------------- | ---------------------------------- |
| Index Page            | `/`             | Overview, login/signup entry point |
| Login Page            | `/login/`       | Login via mobile or code           |
| Signup Page           | `/signup/`      | Register with mobile/email         |
| Dashboard             | `/dashboard/`   | List of contacts/chats             |
| Chat Page             | `/chat/<code>/` | 1-on-1 chat via WebSocket          |
| Audio/Video Call Page | `/call/<code>/` | Start a call (WebRTC)              |


| Feature          | Tech                          |
| ---------------- | ----------------------------- |
| Backend          | Django                        |
| Real-time Chat   | Django Channels (WebSocket)   |
| Audio/Video Call | WebRTC + JS (or Twilio/Agora) |
| Database         | SQLite/PostgreSQL (for prod)  |
| Frontend         | HTML + Tailwind/Bootstrap     |
| Auth             | Custom User (mobile-based)    |
