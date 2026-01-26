#!/usr/bin/env python3
"""
Demo script for Aura MCP Server

This script demonstrates how the MCP server tools work by making actual API calls
to the Aura Gateway (if available) or showing mock responses.
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from server import AuraMCPServer


async def demo_search():
    """Demonstrate the search_hotels tool."""
    print("🔍 Demonstrating search_hotels tool...")
    print("=" * 50)
    
    server = AuraMCPServer()
    
    try:
        # Test search with different queries
        queries = [
            "Luxury beach resort with spa",
            "Budget hotel near airport",
            "Family-friendly resort with pool"
        ]
        
        for query in queries:
            print(f"\n📝 Query: '{query}'")
            result = await server.search_hotels(query, limit=2)
            print(f"📋 Result:\n{result}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        await server.shutdown()


async def demo_negotiation():
    """Demonstrate the negotiate_price tool."""
    print("\n💰 Demonstrating negotiate_price tool...")
    print("=" * 50)
    
    server = AuraMCPServer()
    
    try:
        # Test different negotiation scenarios
        scenarios = [
            ("hotel_alpha", 850.0, "Reasonable bid"),
            ("hotel_beta", 500.0, "Low bid (likely counter)"),
            ("hotel_gamma", 1500.0, "High bid (likely accepted)"),
        ]
        
        for item_id, bid, description in scenarios:
            print(f"\n📝 Scenario: {description}")
            print(f"   Item: {item_id}, Bid: ${bid:.2f}")
            result = await server.negotiate_price(item_id, bid)
            print(f"📋 Result: {result}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        await server.shutdown()


async def demo_complete_workflow():
    """Demonstrate a complete workflow: search then negotiate."""
    print("\n🎯 Demonstrating complete workflow...")
    print("=" * 50)
    
    server = AuraMCPServer()
    
    try:
        # Step 1: Search for hotels
        print("\n🔍 Step 1: Searching for luxury beach resorts...")
        search_result = await server.search_hotels("Luxury beach resort with spa", limit=1)
        print(f"📋 Search Result:\n{search_result}")
        
        # Extract first hotel ID (mock - in real scenario this would parse the actual result)
        # For demo purposes, we'll use a fixed ID
        hotel_id = "hotel_alpha"
        print(f"\n🏨 Selected hotel: {hotel_id}")
        
        # Step 2: Negotiate price
        print("\n💰 Step 2: Negotiating price...")
        initial_bid = 800.0
        print(f"   Initial bid: ${initial_bid:.2f}")
        
        negotiation_result = await server.negotiate_price(hotel_id, initial_bid)
        print(f"📋 Negotiation Result: {negotiation_result}")
        
        # Step 3: Handle counteroffer if needed
        if "COUNTER-OFFER" in negotiation_result:
            print("\n🔄 Step 3: Handling counteroffer...")
            # Extract counteroffer amount (mock parsing)
            counter_bid = 950.0  # Would parse from actual result
            print(f"   Accepting counteroffer: ${counter_bid:.2f}")
            
            final_result = await server.negotiate_price(hotel_id, counter_bid)
            print(f"📋 Final Result: {final_result}")
        
    except Exception as e:
        print(f"❌ Workflow demo failed: {e}")
    finally:
        await server.shutdown()


async def main():
    """Run all demonstrations."""
    print("🚀 Aura MCP Server Demo")
    print("=" * 60)
    print("This demo shows how the MCP server tools work.")
    print("Note: Actual API calls require Aura Gateway to be running.\n")
    
    # Run individual demos
    await demo_search()
    await demo_negotiation()
    
    # Run complete workflow
    await demo_complete_workflow()
    
    print("\n🎉 Demo completed!")
    print("\n📚 Next steps:")
    print("1. Start Aura Gateway: cd api-gateway && uv run python -m src.main")
    print("2. Start MCP Server: cd adapters/mcp-server && python server.py")
    print("3. Connect Claude Desktop to http://localhost:8080")
    print("4. Use the tools in your LLM conversations!")


if __name__ == "__main__":
    asyncio.run(main())