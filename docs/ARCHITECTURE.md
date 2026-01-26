# Aura Platform Architecture

## Overview
Aura is an Agent-Oriented Service Gateway designed to facilitate autonomous economic negotiations between AI agents and service providers.

## Core Components

### System Landscape (C4 Container Diagram)

```mermaid
graph TD
    subgraph Clients ["Clients (The Edge)"]
        Browser["Agent Console (Next.js)"]
        Bot["Autonomous Agent<br>(Python Script)"]
    end

    subgraph Infrastructure ["Aura Platform (Network)"]
        
        %% Entry Point
        Gateway["API Gateway (FastAPI)"]
        style Gateway fill:#f9f,stroke:#333,stroke-width:2px
        
        %% The Brain
        Core["Core Service (gRPC/Python)"]
        style Core fill:#bbf,stroke:#333,stroke-width:2px
        
        %% Storage Layer
        DB[("PostgreSQL\n(pgvector)")]
        Redis[("Redis\n(Cache & State)")]
        
        %% Observability
        Jaeger["Jaeger Tracing"]
    end
    
    subgraph External ["External World"]
        Mistral["Mistral AI API"]
    end

    %% Connections
    Browser -- "HTTP/JSON + Signed Headers" --> Gateway
    Bot -- "HTTP/JSON + Signed Headers" --> Gateway
    
    Gateway -- "gRPC (Protobuf)" --> Core
    Gateway -. "Rate Limiting Check" -.-> Redis
    Gateway -. "Trace Spans" -.-> Jaeger

    Core -- "SQL / Vector Search" --> DB
    Core -- "Get/Set Session & Semantic Cache" --> Redis
    Core -- "LLM Inference" --> Mistral
    Core -. "Trace Spans" -.-> Jaeger

    %% Key
    linkStyle 0,1 stroke-width:2px,fill:none,stroke:green;
    linkStyle 2 stroke-width:4px,fill:none,stroke:blue;
```

### 1. API Gateway (The Diplomat)
- **Tech**: Python / FastAPI / Uvicorn
- **Port**: 8000
- **Role**: 
  - Validates Agent Identity (DID/Tokens).
  - Translates HTTP JSON requests to internal gRPC calls.
  - Handles Rate Limiting.

### 2. Core Engine (The Brain)
- **Tech**: Python / gRPC / LangChain / SQLAlchemy
- **Port**: 50051
- **Role**:
  - Manages `Inventory` and `NegotiationSession`.
  - Executes `PricingStrategy` (Rule-based or LLM-based).
  - Enforces `floor_price` logic.

### 3. Storage Layer
- **PostgreSQL**: Stores inventory items and structured negotiation logs.
- **pgvector** (Planned): Will store semantic embeddings for search.

## Data Flow (Negotiation)

```mermaid
sequenceDiagram
    participant Agent
    participant Gateway
    participant Core
    participant Redis
    participant DB as Postgres (Vector)
    participant AI as Mistral LLM

    Agent->>Gateway: POST /negotiate (Bid: $900, Signed)
    
    Note over Gateway: 1. Verify Signature (Ed25519)<br/>2. Check Rate Limit (Redis)
    
    Gateway->>Core: gRPC Negotiate(item_id, bid)
    
    Note over Core: Start Span (Tracing)
    
    %% Semantic Caching Layer
    Core->>Redis: GET "semantic_hash(item+bid)"
    alt Cache Hit (Fast Path)
        Redis-->>Core: JSON {decision: "counter", price: 950}
        Core-->>Gateway: Response (from Cache)
        Gateway-->>Agent: 200 OK (5ms latency)
    else Cache Miss (Slow Path)
        Core->>DB: SELECT floor_price, embedding FROM items
        DB-->>Core: floor: $800, vec: [...]
        
        Core->>AI: "Analyze Bid $900 vs Floor $800"
        AI-->>Core: {decision: "accept", reasoning: "..."}
        
        par Async Write
            Core->>Redis: SETEX "semantic_hash", TTL=1h
            Core->>DB: INSERT INTO negotiation_logs
        end
        
        Core-->>Gateway: Response (Fresh)
        Gateway-->>Agent: 200 OK (1.5s latency)
    end
```

1. Agent POSTs to `/v1/negotiate`.
2. Gateway converts to Protobuf `NegotiationRequest`.
3. Core Engine fetches Item from DB (including hidden `floor_price`).
4. Strategy evaluates the Bid:
   - If Bid < Floor -> **Counter-Offer**.
   - If Bid > Trigger Limit -> **JIT UI Required**.
   - Else -> **Accept**.
5. Response is returned to Agent.

## Key Decisions
- **Contract-First**: All APIs defined in `proto/aura/negotiation/v1/`.
- **Stateless Strategies**: Logic does not keep state in memory; all context comes from DB.
- **Hidden Knowledge**: Agents never see `floor_price` directly.