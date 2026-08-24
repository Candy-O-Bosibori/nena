# Backend tests

Run with:

```
cd Nena_Back
./venv/bin/python3 -m pytest tests/
```

## Database

Tests run against a dedicated `test` schema inside the same Postgres
database the app already uses locally (`nena`) — no separate database or
extra role privileges required, since the app's `nena_user` role can create
and drop schemas even without `CREATEDB`.

The connection string defaults to:

```
postgresql://nena_user:nena_password@localhost:5432/nena?options=-csearch_path=test
```

Override it with `TEST_DATABASE_URL` if your local setup differs (e.g. a
different user/password, or a separate database if you'd rather not share
`nena`). The `test` schema is created at the start of the session and
dropped at the end; every table is truncated between individual tests so
they never see each other's data.
