
------------------------------------------------------------------------

## Security

### Authentication (NEW in v2.1)

DiagnOStiX runs with high privileges (often root) to perform system repairs. To secure access, **Basic Authentication** is enabled by default.

**Default Credentials:**
- Username: `admin`
- Password: `diagnostix`

**Change these immediately** by setting environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DIAGNOSTIX_USER` | Username for login | `admin` |
| `DIAGNOSTIX_PASSWORD` | Password for login | `diagnostix` |

**Docker Compose Example:**
```yaml
environment:
  - DIAGNOSTIX_USER=myuser
  - DIAGNOSTIX_PASSWORD=mypassword_secure
```

If these are not set, the application will log a warning on startup.

------------------------------------------------------------------------
