# Aura

Aura is a distributed microservices platform for handling negotiations and transactions. It provides a scalable architecture with separate API Gateway and Core Service components, using Protocol Buffers for efficient communication.

## Architecture

- **API Gateway**: Handles incoming requests and routes them to appropriate services
- **Core Service**: Contains the main business logic for negotiation processing
- **Protocol Buffers**: Defines the service interfaces and data structures in `proto/`

## Prerequisites

- Python 3.8+
- uv (Python package manager)
- buf (Protocol Buffer toolkit)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aura
   ```

2. Install Python dependencies:
   ```bash
   uv sync
   ```

3. Install buf:
   ```bash
   # Follow instructions at https://buf.build/docs/installation
   ```

## Building Protocol Buffers

Generate Python code from Protocol Buffer definitions:

```bash
buf generate
```

This will generate gRPC and protobuf Python files in `api-gateway/src/proto/` and `core-service/src/proto/`.

## Running the Services

### Core Service
```bash
cd core-service
uv run python -m src.main
```

### API Gateway
```bash
cd api-gateway
uv run python -m src.main
```

## Development

### Code Generation
After modifying `.proto` files in `proto/`, regenerate the Python code:
```bash
buf generate
```

### Linting
```bash
buf lint
```

### Testing
Add tests in the respective service directories and run with:
```bash
uv run pytest
```

## Project Structure

```
aura/
├── proto/                 # Protocol Buffer definitions
│   ├── aura/
│   │   └── negotiation/
│   │       └── v1/
│   │           └── negotiation.proto
│   ├── buf.yaml          # Buf configuration
│   └── buf.gen.yaml      # Code generation config
├── api-gateway/          # API Gateway service
│   └── src/
│       └── proto/        # Generated protobuf code
├── core-service/         # Core business logic service
│   └── src/
│       └── proto/        # Generated protobuf code
├── pyproject.toml        # Python dependencies
└── uv.lock              # Lock file
```

## Contributing

1. Follow the existing code style
2. Update Protocol Buffers as needed
3. Regenerate code after proto changes
4. Add tests for new functionality
5. Update this README if needed

## License

[Add license information here]