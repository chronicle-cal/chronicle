# Chronicle

Chronicle is a web-based calendar app focused on calendar syncing, managing and smart scheduling.

## Quick start

You can quickly start Chronicle using Docker or Podman. Just run the following command in the root directory of the project:

```bash
docker compose -f compose.yaml up --build
```

## Installation

Please refer to the [Admin Guide](docs/guides/admin.md) for detailed instructions on how to set up Chronicle.

## Architecture

Chronicle is composed of several services that work together to provide the functionality of the application. The main services are:

- `frontend`: The user interface of chronicle. It is a React application that runs in the browser.
- `backend`: The backend service that handles the business logic and API endpoints. It is built with FastAPI and runs on a Python server.
- `worker`: The worker service that handles background tasks such as synchronization with external calendar sources. It is built with Python and runs on a separate server.

## Documentation

The documentation is available in the [docs](docs) directory. It includes guides for installation, administration, and development.

## Versioning

This project uses [Semantic Versioning](https://semver.org/).

## Contributing

Contributions are currently not accepted.

This projects documents architectural decisions via ADRs. You can find them in the [docs/architecture/decisions](docs/architecture/decisions) directory.

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
