<p align="center">
  <img src="artwork/notatka-logo.png" alt="Notatka Logo" />
</p>

**Notatka** is a powerful note-taking service designed to help users efficiently manage their notes and stay organized. Built as a monorepo with three microservices, Notatka aims to provide a seamless experience for users across various functionalities such as authentication, notifications, and notes management.

### Account

**Description:** responsible for authorization and data
users. All other services depend on it, it issues the JWT token and performs introspection.

**Key Features:**
- [x] User registration and login
- [x] JWT token issuance and validation
- [x] User profile management
- [x] Password reset functionality

### Notifications

**Description:** Manages user notifications, ensuring that users are informed about important events related to their notes and account activities.

**Key Features:**
- [x] Email notifications for important events
- [ ] User preferences for notification settings

### Notes

**Description:** Handles all functionalities related to note creation, editing, and organization. This service allows users to create, update, delete, and retrieve their notes efficiently.

**Key Features:**
- [x] Create, read, update, and delete (CRUD) operations for notes
- [ ] Tagging and categorization of notes
- [ ] Search functionality to find notes quickly
- [ ] Collaboration features for sharing notes with other users

### Getting Started

1) Clone the repository and navigate to the directory:
    ```bash
    git clone git@guthub.com:ivan-karaberov/notatka
    cd notatka
    ```

2) Copy notifications/core/.env.example to notifications/core/.env and edit the .env file, populating it with all environment variables:

    ```bash
    cp notifications/src/core/.env.example notifications/src/core/.env
    ```

3) Run the services:

    ```bash
    docker compose up

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential improvements or features.

### License

[CC BY-NC-SA 4.0](https://github.com/ivan-karaberov/notatka/blob/master/LICENSE)


TLDR:
- Clone and Use for Free: You are welcome to clone this repository and use it for your own purposes at no cost.
- You can fork and change it (attribution and same license required)
- You cannot sell it, it would not be fair
