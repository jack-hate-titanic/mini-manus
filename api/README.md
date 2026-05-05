# API Development

## Environment

```bash
cd /Users/wson/Desktop/mini-manus/api
make sync
```

## Run the API

```bash
cd /Users/wson/Desktop/mini-manus/api
make run
```

## Database Migrations

Alembic is configured to read the database URL from `core.config.Settings`, which
currently resolves from `.env`. Runtime database access keeps using the async
`asyncpg` URL, while Alembic automatically converts it to a synchronous
`psycopg2` URL for migrations.

Create a new migration from model changes:

```bash
cd /Users/wson/Desktop/mini-manus/api
make revision m="describe your change"
```

Apply migrations:

```bash
cd /Users/wson/Desktop/mini-manus/api
make upgrade
```

Rollback the most recent migration:

```bash
cd /Users/wson/Desktop/mini-manus/api
make downgrade
```

Show the current migration version:

```bash
cd /Users/wson/Desktop/mini-manus/api
make current
```
