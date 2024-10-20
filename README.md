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
- [ ] Create, read, update, and delete (CRUD) operations for notes
- [ ] Tagging and categorization of notes
- [ ] Search functionality to find notes quickly
- [ ] Collaboration features for sharing notes with other users

### Notes

**Description:** Handles all functionalities related to note creation, editing, and organization. This service allows users to create, update, delete, and retrieve their notes efficiently.

**Key Features:**
- [x] Email notifications for important events
- [ ] User preferences for notification settings

### Getting Started

To get started with Notatka, clone the repository and follow the setup instructions in the respective microservice directories. Ensure that you have the necessary environment variables configured for each service.

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential improvements or features.

### License

This project is licensed under the MIT License
