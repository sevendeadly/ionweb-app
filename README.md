# Hello World Containerized Application

This is a simple containerized application that displays "Hello world, {name}" where {name} is retrieved from a PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Building and Running the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd hello-world-app
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
- Open your web browser and navigate to: http://localhost:5050
- You should see a JSON response with "Hello world, John Doe"

## Running Tests

## Running Tests with Docker

1. Ensure containers are running:
```bash
docker-compose up -d
```

2. Execute tests in web container:
```bash
docker-compose exec web pytest tests/ -v
```

Additional testing options:
```bash
# Run with coverage
docker-compose exec web pytest tests/ -v --cov=backend

# Run specific test file
docker-compose exec web pytest tests/test_app.py

# Run with specific pattern
docker-compose exec web pytest -k "connection" tests/

# Generate coverage report
docker-compose exec web pytest tests/ --cov=backend --cov-report=html
```

Dependencies:
- pytest
- pytest-cov (for coverage reports)


## Project Structure

- `backend/`: Contains the Flask web application
- `database/`: Contains the PostgreSQL initialization script
- `tests/`: Contains the test files
- `docker-compose.yml`: Defines the multi-container Docker application
- `README.md`: This file

## Security Considerations

1. **Environment Variables**
   - Use `.env` files for local development
   - Use secrets management in production (e.g., Kubernetes Secrets, HashiCorp Vault)
   - Never commit `.env` files to version control

2. **Database Security**
   - Use strong passwords
   - Restrict network access to database
   - Regular security updates
   - Implement connection pooling
   - Use least privilege principle

3. **Application Security**
   - Regular dependency updates
   - Input validation
   - Error handling without exposing sensitive info
   - HTTPS in production
   - Rate limiting

## Development

```bash
# Install dependencies
make install

# Build and run
make build
make run

# Cleanup
make clean
```

## CI/CD Configuration

1. Implement automated testing : we could implement GitHub Actions to run tests on every push to the repository.
   - Will build the Docker containers before continuing with other jobs
2. Security scanning: 
   - Could use Bandit for Python code scanning for vulnerabilties and security issues such as hardcoded secrets and SQL injection in the database handling the names.
3. Container image scanning:
    - Also, we could use Trivy to scan Docker images for vulnerabilities
4. Infrastructure as Code validation:

## Monitoring Considerations

1. Application metrics
2. Database metrics
3. Container health
4. Log aggregation

---
# .gitignore
__pycache__/
*.pyc
.coverage
.env
.pytest_cache/
*.log

## Stopping the Application

To stop the application and remove all data:
```bash
docker-compose down -v
```

## Contributing

Feel free to submit issues and enhancement requests!

## Reference

All code in this project is original and was created for this specific implementation. However, the idea for this project was inspired by various tutorials and resources online.