# DigiBoom

Corporate website and CMS for [digiboom.az](https://www.digiboom.az).

DigiBoom manages digital services, portfolio, trainings, packages, and blog content from the admin panel. The site runs in three languages: **Azerbaijani**, **English**, and **Russian**.

## Features

- Home, About, Services, Portfolio, Trainings, Blog, Contact
- Service, training, and project detail pages
- Package orders, training orders, consultation and contact submissions
- Review form
- Privacy policy and terms of use (footer links appear when the texts are filled in)
- Cloudflare Turnstile (when keys are set)
- Full content management from admin (CKEditor, image compression, inline help)

## Stack

| | |
|---|---|
| Backend | Django 5.2+, Python 3.11+ |
| Database | PostgreSQL 15 |
| WSGI | Gunicorn |
| Front end | HTML templates, Bootstrap, jQuery, AOS |
| Editing | django-ckeditor |
| Media | Pillow, django-cleanup |
| Packaging | `uv` (`pyproject.toml` / `uv.lock`) |
| Deploy | Docker Compose + Nginx |

## Layout

```
Digiboom/
├── docker/                  # Dockerfile, compose, entrypoint
├── nginx/                   # Production reverse proxy + SSL
├── digiboom/
│   ├── manage.py
│   ├── core/                # Models, views, admin, form APIs
│   ├── digiboom/            # Settings, URLs, WSGI, middleware
│   ├── templates/           # Page and include templates
│   ├── static/              # CSS, JS, images
│   ├── locale/              # EN / RU gettext catalogs
│   └── media/               # Uploads (gitignored)
├── pyproject.toml
└── uv.lock
```

`core` is split by domain: `models/`, `views/`, `admin/admin_v1/`, `utils/`. CMS fields follow `name_az` / `name_en` / `name_ru` (same pattern for `title_*`, `text_*`, and so on).

## Pages and APIs

| URL | Description |
|---|---|
| `/` | Home |
| `/about/` | About |
| `/services/`, `/services/<slug>/` | Services |
| `/portfolio/`, `/portfolio/<slug>/` | Portfolio |
| `/training/`, `/training/<slug>/` | Trainings |
| `/blog/`, `/blog/<slug>/` | Blog |
| `/contact/` | Contact |
| `/privacy/`, `/terms/` | Legal pages |
| `/i18n/setlang/` | Language switch |
| `/api/appeal/` | Contact / inquiry |
| `/api/consultation/` | Consultation |
| `/api/package-order/` | Package order |
| `/api/training-order/` | Training order |
| `/api/review/` | Review |

The admin path is **not** `/admin/` by default in production. Set a non-obvious value in `ADMIN_URL` and do not publish it.

## Requirements

- Docker and Docker Compose (recommended)
- or Python 3.11+, `uv`, PostgreSQL 15
- For production: `fullchain.pem` and `privkey.pem` under `nginx/ssl/`

## Environment variables

`docker/.env` is gitignored. Compose and local settings read from it.

**Required**

| Variable | Notes |
|---|---|
| `SECRET_KEY` | Django secret — never commit or share the real value |
| `ADMIN_URL` | Hidden admin path, trailing slash required. Use a unique path in production, not `admin/` |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | User |
| `POSTGRES_PASSWORD` | Password |
| `POSTGRES_HOST` | Usually `db` in Docker |
| `POSTGRES_PORT` | `5432` on the Docker network |

**Optional**

| Variable | Default / notes |
|---|---|
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | `digiboom.az,www.digiboom.az,localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Extra origins (comma-separated) |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP |
| `EMAIL_USE_TLS` / `EMAIL_USE_SSL` | `True` / `False` |
| `DEFAULT_FROM_EMAIL` | Sender address |
| `CONTACT_RECEIVER_EMAIL` | Inbox for inquiries |
| `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile |
| `SITE_NAME` | `DigiBoom` |
| `SITE_DOMAIN` | `www.digiboom.az` |

The local compose file sets **local-only** defaults (`DEBUG=True`, a local `ADMIN_URL`, database `digiboom_local`). Do not reuse those values in production. Production compose needs a complete `.env` with unique secrets.

## Local setup (Docker)

```bash
cd docker
docker compose -f docker-compose-local.yaml up --build
```

- Site: [http://localhost:8000](http://localhost:8000)
- PostgreSQL on the host: `localhost:5433` (`5432` inside the container; local compose only)
- Admin: `http://localhost:8000/<ADMIN_URL>` from your local `.env`

Create a superuser:

```bash
docker exec -it digiboom_web_local python digiboom/manage.py createsuperuser
```

Stop:

```bash
docker compose -f docker-compose-local.yaml down
```

## Production (Docker)

Put SSL certificates in `nginx/ssl/`, fill in `docker/.env`, then:

```bash
cd docker
docker compose -f docker-compose.yaml up --build -d
```

Services: PostgreSQL → Gunicorn (`web`) → Nginx (`80` / `443`). Nginx redirects to HTTPS and serves `/static/` and `/media/` directly. Upload limit is `130M`.

`migrate` and `collectstatic` run automatically when the container starts.

## Without Docker

```bash
uv sync
export DJANGO_SETTINGS_MODULE=digiboom.settings_local
cd digiboom
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`settings_local.py` reads `docker/.env`. PostgreSQL must be reachable.

## Admin and content

The admin UI is in Azerbaijani. Content is stored in three languages:

- `*_az` — required
- `*_en`, `*_ru` — if empty, the site falls back to AZ

In templates, CMS strings are resolved with:

```django
{{ service|localized:'name' }}
```

Fixed UI strings (`Services`, `Online Trainings`, and so on) use `{% trans %}` plus the `locale/en` and `locale/ru` `.po` files.

### Test data

Wipe CMS content and load sample records:

```bash
python digiboom/manage.py seed_cms_test_data
```

This deletes and recreates About, services, projects, trainings, blog, and similar content. Submissions, orders, and reviews are kept. Use it only in local/test environments.

## Translations

```bash
cd digiboom
python manage.py makemessages -l en -l ru
python manage.py compilemessages
```

`makemessages` / `compilemessages` need GNU gettext (`msgfmt`) on the system. Docker images already include `gettext`.

After adding a `{% trans "..." %}` string, put `msgid` / `msgstr` in the `.po` files and run `compilemessages`. Editing `.po` alone is not enough — `.mo` must be rebuilt.

Supported languages: `az` (default), `en`, `ru`. The active language is stored in the session (`/i18n/setlang/`).

## Useful commands

```bash
python digiboom/manage.py migrate
python digiboom/manage.py collectstatic --noinput
python digiboom/manage.py createsuperuser
python digiboom/manage.py compilemessages -l en -l ru
```

Inside Docker, run the same commands as `python digiboom/manage.py ...` in the `digiboom_web` or `digiboom_web_local` container.

## Security

- Never commit `.env`, SSL keys, `SECRET_KEY`, DB passwords, SMTP passwords, or Turnstile **secret** keys.
- Production: `DEBUG=False`, unique `SECRET_KEY`, unique `ADMIN_URL`, strong DB password.
- Do not expose PostgreSQL to the public internet. Local compose maps `5433` only for development.
- Treat `ADMIN_URL` as secret. A public README or chat should not contain the live admin path.
- `TURNSTILE_SITE_KEY` is public; `TURNSTILE_SECRET_KEY` is not.
- `seed_cms_test_data` is for local/test only — it wipes CMS content.

`media/` and `staticfiles/` are gitignored. Uploaded images are compressed in admin. `django-cleanup` removes media files from disk when records are deleted.
