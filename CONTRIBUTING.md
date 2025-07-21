# Contributing to Japapou

Thanks for considering contributing to this project! 🎉  
We welcome all kinds of contributions, including code, design, documentation, and suggestions.

## 📦 Setting Up the Project

1. **Fork the repository** and clone it:

    ```bash
    git clone https://github.com/PI-InfoWeb-CNAT/Japapou.git
    cd Japapou
    ```

2. **Set up your environment** (adjust as needed for your stack):

    ```bash
    python -m venv venv
    venv/scripts/activate
    pip install -r requirements.txt
    ```

3. **Run the project locally**:

    ```bash
    python source/manage.py runserver
    ```

## 🌿 Branching Strategy

We use a simple branching strategy:

-   The `main` branch holds all production-ready and working code.
-   Do **not** commit directly to `main`.
-   Create a new branch for every new feature or bugfix.
-   Use one of the following naming conventions:
    -   `feature/your-feature-name`
    -   `bug/short-bug-description`

### ✅ How to Create a Branch

1. Make sure your local `main` is up to date:

    ```bash
    git checkout main
    git pull origin main
    ```

2. Create and switch to a new branch:

    - For a new **feature**:

        ```bash
        git checkout -b feature/feature-name
        ```

    - For a **bug fix**:

        ```bash
        git checkout -b bug/bug-description
        ```

3. Do your work and commit normally:

    ```bash
    git add .
    git commit -m "feat: add login form"
    ```

4. Push your branch to GitHub:

    ```bash
    git push -u origin feature/feature-name
    # or
    git push -u origin bug/bug-description
    ```

5. Open a pull request to merge your branch into `main`.

## ✍️ Commit Guidelines

Write clear, present-tense commit messages that describe what the change does.

Each commit should focus on **one purpose**: a single feature, bug fix, or update.

### ✅ Commit Format

```
type: short summary of the change
(optional) longer explanation of what and why
```

**Common `type` values:**

-   `feat`: New feature
-   `fix`: Bug fix
-   `docs`: Documentation changes only
-   `style`: Code style or formatting (no logic changes)
-   `refactor`: Code changes that don’t add or fix a feature
-   `test`: Adding or improving tests

### ✅ Example Commits

```
feat: add login form with email validation

fix: prevent crash when submitting empty password

docs: update README with setup instructions

style: format signup form with 2-space indentation
```

Yes, that's mostly correct — just a couple of small formatting and clarity improvements to make it cleaner and fully consistent with markdown and best practices.

Here’s a polished version:

## ✅ Pull Requests

1. Make sure your branch is **up to date** with `main`:

    ```bash
    git fetch origin
    git merge origin/main
    ```

2. Open a pull request with a **clear title and description**.

3. Link related issues using `Closes #issue_number` when applicable.

4. Submit **one pull request per feature or bug fix**.

5. Keep pull requests **small and focused** to make reviewing easier.

## 🐛 Reporting Issues

When submitting a bug or feature request:

-   Use the GitHub Issues tab.
-   Include clear steps to reproduce (if it's a bug).
-   Suggest a fix or improvement if you have one.

## 💡 Code Style

-   Follow the [STYLE_GUIDE.md](STYLE_GUIDE.md) if available.
-   Use consistent indentation (e.g., 2 or 4 spaces).
-   Name things clearly.
-   Write docstrings and comments where appropriate.

## 🙏 Thank You

You're helping make this project better for everyone.
Feel free to ask questions — we're happy to help.

```

```
