"""
MCP Server for Aura Platform

This server acts as a proxy between AI models (via MCP) and the Aura Gateway,
providing search and negotiation capabilities to LLMs like Claude 3.5 Sonnet.
"""

import asyncio
import logging
import os
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv

# Import AgentWallet from parent directory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from agent_identity import AgentWallet

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("aura-mcp-server")

# Load environment variables
load_dotenv()

# Configuration
GATEWAY_URL = os.getenv("AURA_GATEWAY_URL", "http://localhost:8000")
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8080"))

class AuraMCPServer:
    """
    MCP Server that exposes Aura Platform capabilities to AI models.
    
    This server acts as a proxy client that:
    1. Generates a temporary Ed25519 wallet on startup
    2. Signs all requests to the Aura Gateway
    3. Exposes search and negotiation tools via MCP
    4. Handles errors gracefully for LLM consumption
    """
    
    def __init__(self):
        """Initialize the MCP server and HTTP client."""
        self.wallet = AgentWallet()  # Generate temporary wallet
        self.client = httpx.AsyncClient(timeout=30.0)
        
        logger.info("🔑 Generated temporary agent wallet")
        logger.info(f"   DID: {self.wallet.did}")
        logger.info(f"   Public Key: {self.wallet.public_key_hex}")
        
        # Initialize MCP server
        self.mcp_server = self._initialize_mcp_server()
    
    def _initialize_mcp_server(self):
        """Initialize the MCP server with Aura tools."""
        try:
            # Try to import MCP (might need to install first)
            from mcp import FastMCP, Tool
            
            # Create MCP server
            mcp = FastMCP(
                name="Aura",
                description="Aura Platform - AI-powered negotiation and search system",
                version="1.0.0"
            )
            
            # Register tools
            mcp.register_tool(
                Tool(
                    name="search_hotels",
                    description="Search for hotels matching a query",
                    parameters={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for hotels"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    },
                    func=self.search_hotels
                )
            )
            
            mcp.register_tool(
                Tool(
                    name="negotiate_price",
                    description="Negotiate price for a specific hotel/item",
                    parameters={
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "string",
                                "description": "ID of the item to negotiate"
                            },
                            "bid": {
                                "type": "number",
                                "description": "Bid amount in USD",
                                "minimum": 0.01
                            }
                        },
                        "required": ["item_id", "bid"]
                    },
                    func=self.negotiate_price
                )
            )
            
            return mcp
            
        except ImportError as e:
            logger.warning(f"⚠️  MCP package not found: {e}")
            logger.info("🔧 Using mock MCP implementation for development")
            
            # Fall back to mock implementation
            from mock_mcp import FastMCP, Tool
            
            # Create mock MCP server
            mcp = FastMCP(
                name="Aura (Mock)",
                description="Aura Platform - AI-powered negotiation and search system (Mock Mode)",
                version="1.0.0"
            )
            
            # Register tools
            mcp.register_tool(
                Tool(
                    name="search_hotels",
                    description="Search for hotels matching a query",
                    parameters={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for hotels"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    },
                    func=self.search_hotels
                )
            )
            
            mcp.register_tool(
                Tool(
                    name="negotiate_price",
                    description="Negotiate price for a specific hotel/item",
                    parameters={
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "string",
                                "description": "ID of the item to negotiate"
                            },
                            "bid": {
                                "type": "number",
                                "description": "Bid amount in USD",
                                "minimum": 0.01
                            }
                        },
                        "required": ["item_id", "bid"]
                    },
                    func=self.negotiate_price
                )
            )
            
            return mcp
    
    async def search_hotels(self, query: str, limit: int = 3) -> str:
        """
        Search hotels via Aura Gateway.
        
        Args:
            query: Search query string
            limit: Maximum number of results (default: 3)
            
        Returns:
            Formatted string with search results for LLM consumption
        """
        logger.info(f"🔍 Searching hotels: '{query}' (limit: {limit})")
        
        body = {
            "query": query,
            "limit": limit
        }
        
        try:
            # Sign the request
            agent_id, timestamp, signature = self.wallet.sign_request(
                "POST", "/v1/search", body
            )
            
            # Make request to Aura Gateway
            response = await self.client.post(
                f"{GATEWAY_URL}/v1/search",
                json=body,
                headers={
                    "X-Agent-ID": agent_id,
                    "X-Timestamp": timestamp,
                    "X-Signature": signature,
                    "Content-Type": "application/json"
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Format results for LLM
            results = []
            for item in data.get("results", []):
                results.append(
                    f"{item['name']} - ${item['price']:.2f} "
                    f"(Relevance: {item['score']:.2f}) - {item.get('details', 'No details')}"
                )
            
            if results:
                return "🏨 Search Results:\n" + "\n".join(results)
            else:
                return "No hotels found matching your criteria."
                
        except httpx.HTTPStatusError as e:
            logger.error(f"🔴 Gateway error: {e}")
            return f"❌ Search failed: Gateway returned error {e.response.status_code}"
        except httpx.RequestError as e:
            logger.error(f"🔴 Network error: {e}")
            return "❌ Search failed: Could not connect to Aura Gateway"
        except Exception as e:
            logger.error(f"🔴 Unexpected error: {e}")
            return f"❌ Search failed: {str(e)}"
    
    async def negotiate_price(self, item_id: str, bid: float) -> str:
        """
        Negotiate price for an item via Aura Gateway.
        
        Args:
            item_id: ID of the item to negotiate
            bid: Bid amount in USD
            
        Returns:
            Formatted string with negotiation result for LLM consumption
        """
        logger.info(f"💰 Negotiating {item_id}: ${bid:.2f}")
        
        body = {
            "item_id": item_id,
            "bid_amount": bid,
            "currency": "USD",
            "agent_did": self.wallet.did
        }
        
        try:
            # Sign the request
            agent_id, timestamp, signature = self.wallet.sign_request(
                "POST", "/v1/negotiate", body
            )
            
            # Make request to Aura Gateway
            response = await self.client.post(
                f"{GATEWAY_URL}/v1/negotiate",
                json=body,
                headers={
                    "X-Agent-ID": agent_id,
                    "X-Timestamp": timestamp,
                    "X-Signature": signature,
                    "Content-Type": "application/json"
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Handle polymorphic responses
            status = data.get("status")
            
            if status == "accepted":
                reservation_code = data["data"].get("reservation_code", "unknown")
                return f"🎉 SUCCESS! Reservation: {reservation_code}"
            
            elif status == "countered":
                proposed_price = data["data"].get("proposed_price", bid)
                message = data["data"].get("message", "No reason provided")
                return (f"🔄 COUNTER-OFFER: ${proposed_price:.2f}. "
                       f"Message: {message}")
            
            elif status == "ui_required":
                template = data["action_required"].get("template", "unknown")
                return f"🚨 HUMAN INTERVENTION REQUIRED. Template: {template}"
            
            elif status == "rejected":
                return "🚫 REJECTED"
            
            else:
                return f"❓ Unknown negotiation status: {status}"
                
        except httpx.HTTPStatusError as e:
            logger.error(f"🔴 Gateway error: {e}")
            return f"❌ Negotiation failed: Gateway returned error {e.response.status_code}"
        except httpx.RequestError as e:
            logger.error(f"🔴 Network error: {e}")
            return "❌ Negotiation failed: Could not connect to Aura Gateway"
        except Exception as e:
            logger.error(f"🔴 Unexpected error: {e}")
            return f"❌ Negotiation failed: {str(e)}"
    
    async def run(self):
        """Run the MCP server."""
        logger.info(f"🚀 Starting MCP server on {MCP_HOST}:{MCP_PORT}")
        logger.info(f"🔗 Connecting to Aura Gateway at {GATEWAY_URL}")
        
        try:
            # Start the MCP server
            await self.mcp_server.start(
                host=MCP_HOST,
                port=MCP_PORT
            )
        except Exception as e:
            logger.error(f"❌ Failed to start MCP server: {e}")
            raise
    
    async def shutdown(self):
        """Clean up resources."""
        logger.info("🛑 Shutting down MCP server...")
        await self.client.aclose()
        if hasattr(self.mcp_server, 'shutdown'):
            await self.mcp_server.shutdown()

async def main():
    """Main entry point."""
    server = AuraMCPServer()
    
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("🔘 Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())