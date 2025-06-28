<br />
<div align="center">
<h3 align="center">📊 VoteApp</h3>

  <p align="center">
     A simple and minimal voting application built with Python.
  </p>
</div>

---

### 🚀 Overview

**VoteApp** is a lightweight application designed to handle basic voting functionalities.

🧩 **Current Features:**

- Create a member account, and events with 2-4 choice per event
- Auth token JWT 
- (More features coming soon...)

### 🛠 Tech Stack

- [`FastAPI`](https://fastapi.tiangolo.com/) – high-performance web framework for APIs
  
- [`SQLModel`](https://sqlmodel.tiangolo.com/) – ORM and data modeling library built on SQLAlchemy and Pydantic  

- [`pydantic`](https://pydantic-docs.helpmanual.io/) – Data validation and settings management using Python type annotations  

- [`passlib`](https://passlib.readthedocs.io/en/stable/) – Secure password hashing library; using `bcrypt` for robust authentication 

- [`PyJWT`](https://pyjwt.readthedocs.io/en/stable/) – JSON Web Token implementation in Python for secure token-based authentication  

- [`black`](https://github.com/psf/black) and [`isort`](https://github.com/PyCQA/isort) – code formatting

---

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