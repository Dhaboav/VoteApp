<br />
<div align="center">
  <h3 align="center">📊 VoteApp</h3>

  <p align="center">
    A simple and minimal voting application built with Python and FastAPI.
  </p>
</div>

---

## 🚀 Overview

**VoteApp** is a lightweight application designed to handle basic voting functionalities. It offers a clean and simple interface for creating voting events and allowing users to vote securely using event IDs.

### 🔑 Current Features

- 🔐 User registration and authentication with JWT
- 🗳️ Create and manage voting events
- ✅ Vote by event ID
- 📈 Minimal and efficient API endpoints
- 🧩 More features coming soon...

---

## 🛠 Tech Stack

- [`FastAPI`](https://fastapi.tiangolo.com/) – High-performance web framework for building APIs
- [`SQLModel`](https://sqlmodel.tiangolo.com/) – ORM and data modeling (built on SQLAlchemy + Pydantic)
- [`pydantic`](https://pydantic-docs.helpmanual.io/) – Data validation using Python type hints
- [`passlib`](https://passlib.readthedocs.io/en/stable/) – Secure password hashing (using `bcrypt`)
- [`PyJWT`](https://pyjwt.readthedocs.io/en/stable/) – JSON Web Token implementation for auth
- [`black`](https://github.com/psf/black) & [`isort`](https://github.com/PyCQA/isort) – Code formatting tools


### 📦 Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Dhaboav/VoteApp.git
    ```

2. **Install dependencies with Poetry:**

    ```bash
    poetry install
    ```

2. **Run the application:**

    ```bash
    poetry run start
    ```

3. **Copy environment file:**

    ```bash
    copy .env.example .env
    ```

4. **Generate Secret Key:**

    ```bash
    openssl rand -hex 32
    ```
---

### License

This project is licensed under the [MIT License](LICENSE).