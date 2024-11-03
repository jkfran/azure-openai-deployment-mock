# Azure OpenAI Deployment Mock

This project emulates or mocks Azure OpenAI API deployments for testing and development purposes.

## Features

- Mock both streaming and non-streaming responses.
- Simulate token-based streaming for testing real-time API behaviors.

## Requirements

- Docker
- Python 3.12 (for local development)

## Setup and Usage

### Running with Docker

To run this mock API using Docker, you can either pull the pre-built image directly from Docker Hub or build it locally:

#### Option 1: Run with Pre-Built Image

Pull and run the Docker container from Docker Hub:

```bash
docker run -p 8000:8000 jkfran/azure-openai-mock-api
```

The API will be available at `http://localhost:8000`.

#### Option 2: Build and Run Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jkfran/azure-openai-deployment-mock.git
   cd azure-openai-deployment-mock
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t azure-openai-mock-api .
   ```

3. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 azure-openai-mock-api
   ```

### Access the API

The API will be available at `http://localhost:8000`. You can interact with it using tools like Postman or curl.

### API Endpoints

#### POST `/openai/deployments/{model_name}/chat/completions`

This endpoint simulates an OpenAI completion request.

##### Request Headers:

- `api-key`: A required header to authenticate requests. You can use `MOCK-AZURE-OPENAI-API-KEY-1234567890` as the valid key.

##### Request Body:

- **stream**: Set to `true` to enable streaming responses. Default is `false`.

#### Example Request:

```bash
curl -X POST "http://localhost:8000/openai/deployments/mock-deployment/chat/completions" \
     -H "api-key: MOCK-AZURE-OPENAI-API-KEY-1234567890" \
     -d '{ "stream": true }'
```

### Local Development

To run the API locally without Docker, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn mock_api:app --reload --host 0.0.0.0 --port 8000
```

### Contributing

Contributions are welcome! If you'd like to improve the mock API or add more features, feel free to fork the repository, make your changes, and open a pull request.

1. Fork the project.
2. Create a feature branch.
3. Submit a pull request.

### License

This project is open source and available under the [MIT License](LICENSE).
