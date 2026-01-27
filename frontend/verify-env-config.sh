#!/bin/bash
# Verification script for frontend GATEWAY_URL configuration

echo "==================================="
echo "Frontend Environment Configuration Verification"
echo "==================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check 1: Environment files exist
echo "1. Checking environment files..."
if [ -f ".env.example" ]; then
  echo -e "${GREEN}✓${NC} .env.example exists"
  cat .env.example | sed 's/^/  /'
else
  echo -e "${RED}✗${NC} .env.example missing"
fi

if [ -f ".env.local" ]; then
  echo -e "${GREEN}✓${NC} .env.local exists"
  cat .env.local | sed 's/^/  /'
else
  echo -e "${YELLOW}⚠${NC} .env.local not found (optional for development)"
fi

if [ -f ".env.production" ]; then
  echo -e "${GREEN}✓${NC} .env.production exists"
  cat .env.production | sed 's/^/  /'
else
  echo -e "${RED}✗${NC} .env.production missing"
fi

echo ""

# Check 2: TypeScript type definitions
echo "2. Checking TypeScript type definitions..."
if [ -f "env.d.ts" ]; then
  echo -e "${GREEN}✓${NC} env.d.ts exists"
  echo "  Checking TypeScript compilation..."
  npx tsc --noEmit 2>&1 | head -5
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} TypeScript compilation successful"
  else
    echo -e "${RED}✗${NC} TypeScript compilation has errors"
  fi
else
  echo -e "${RED}✗${NC} env.d.ts missing"
fi

echo ""

# Check 3: GitIgnore configuration
echo "3. Checking .gitignore configuration..."
if grep -q ".env.*.local" .gitignore; then
  echo -e "${GREEN}✓${NC} .env*.local is gitignored"
else
  echo -e "${RED}✗${NC} .env*.local not in .gitignore"
fi

echo ""

# Check 4: BrowserAgentWallet implementation
echo "4. Checking BrowserAgentWallet implementation..."
if grep -q "process.env.NEXT_PUBLIC_API_GATEWAY_URL" src/lib/agent-wallet.ts; then
  echo -e "${GREEN}✓${NC} Environment variable is used in agent-wallet.ts"
else
  echo -e "${RED}✗${NC} Hardcoded URL detected in agent-wallet.ts"
fi

echo ""

# Check 5: Docker Compose configuration
echo "5. Checking Docker Compose configuration..."
cd ..
if grep -q "NEXT_PUBLIC_API_GATEWAY_URL.*api-gateway:8000/v1" compose.yml; then
  echo -e "${GREEN}✓${NC} Docker Compose has correct environment variable"
  grep "NEXT_PUBLIC_API_GATEWAY_URL" compose.yml | sed 's/^/  /'
else
  echo -e "${RED}✗${NC} Docker Compose environment variable incorrect"
fi

echo ""

# Check 6: Kubernetes deployment
echo "6. Checking Kubernetes deployment configuration..."
if [ -f "deploy/aura/templates/frontend.yaml" ]; then
  if grep -q "NEXT_PUBLIC_API_GATEWAY_URL" deploy/aura/templates/frontend.yaml; then
    echo -e "${GREEN}✓${NC} Kubernetes deployment has environment variable"
    grep -A1 "NEXT_PUBLIC_API_GATEWAY_URL" deploy/aura/templates/frontend.yaml | sed 's/^/  /'
  else
    echo -e "${RED}✗${NC} Kubernetes deployment missing environment variable"
  fi
fi

if [ -f "deploy/aura/values.yaml" ]; then
  if grep -q "apiGatewayUrl" deploy/aura/values.yaml; then
    echo -e "${GREEN}✓${NC} Helm values.yaml has apiGatewayUrl"
    grep "apiGatewayUrl" deploy/aura/values.yaml | sed 's/^/  /'
  else
    echo -e "${RED}✗${NC} Helm values.yaml missing apiGatewayUrl"
  fi
fi

echo ""
echo "==================================="
echo "Verification Complete"
echo "==================================="
