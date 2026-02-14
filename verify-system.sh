#!/bin/bash

# HRMS System Verification Script
# This script checks if all components are properly set up

echo "🔍 HRMS System Verification"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check Backend Files
echo "📦 Checking Backend Files..."
echo "----------------------------"

BACKEND_DOMAINS=(
    "backend/app/contexts/hrms/domain/employee.py"
    "backend/app/contexts/hrms/domain/leave.py"
    "backend/app/contexts/hrms/domain/working_schedule.py"
    "backend/app/contexts/hrms/domain/work_location.py"
    "backend/app/contexts/hrms/domain/public_holiday.py"
    "backend/app/contexts/hrms/domain/deduction_rule.py"
)

for file in "${BACKEND_DOMAINS[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Domain: $(basename $file)"
    else
        check_fail "Missing: $file"
    fi
done

BACKEND_ROUTES=(
    "backend/app/contexts/hrms/routes/employee_route.py"
    "backend/app/contexts/hrms/routes/leave_route.py"
    "backend/app/contexts/hrms/routes/working_schedule_route.py"
    "backend/app/contexts/hrms/routes/work_location_route.py"
    "backend/app/contexts/hrms/routes/public_holiday_route.py"
    "backend/app/contexts/hrms/routes/deduction_rule_route.py"
)

for file in "${BACKEND_ROUTES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Route: $(basename $file)"
    else
        check_fail "Missing: $file"
    fi
done

echo ""

# 2. Check Frontend Files
echo "🎨 Checking Frontend Files..."
echo "----------------------------"

FRONTEND_PAGES=(
    "frontend/src/pages/hr/index.vue"
    "frontend/src/pages/hr/employees/employee-profile.vue"
    "frontend/src/pages/hr/leaves/index.vue"
)

for file in "${FRONTEND_PAGES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Page: $(basename $file)"
    else
        check_fail "Missing: $file"
    fi
done

FRONTEND_API=(
    "frontend/src/api/hr_admin/employee"
    "frontend/src/api/hr_admin/leave"
    "frontend/src/api/hr_admin/schedule"
)

for dir in "${FRONTEND_API[@]}"; do
    if [ -d "$dir" ]; then
        check_pass "API Service: $(basename $dir)"
    else
        check_warn "Missing: $dir (optional)"
    fi
done

echo ""

# 3. Check Docker Setup
echo "🐳 Checking Docker Setup..."
echo "----------------------------"

if [ -f "backend/docker-compose.yml" ]; then
    check_pass "docker-compose.yml exists"
else
    check_fail "docker-compose.yml not found"
fi

if [ -f "backend/.env" ]; then
    check_pass ".env file exists"
else
    check_warn ".env file not found (will use defaults)"
fi

echo ""

# 4. Check if services are running
echo "🚀 Checking Running Services..."
echo "----------------------------"

# Check if backend is running
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    check_pass "Backend API is running (port 5001)"
else
    check_warn "Backend API is not running (port 5001)"
    echo "   Run: cd backend && docker-compose up"
fi

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    check_pass "Frontend is running (port 3000)"
else
    check_warn "Frontend is not running (port 3000)"
    echo "   Run: cd frontend && pnpm dev"
fi

# Check if MongoDB is accessible
if docker ps | grep -q mongo; then
    check_pass "MongoDB container is running"
else
    check_warn "MongoDB container is not running"
fi

echo ""

# 5. Summary
echo "📊 Summary"
echo "=============================="
echo ""

if [ -f "backend/app/contexts/hrms/routes/employee_route.py" ] && \
   [ -f "frontend/src/pages/hr/employees/employee-profile.vue" ]; then
    echo -e "${GREEN}✓ Employee Management: Ready${NC}"
else
    echo -e "${RED}✗ Employee Management: Incomplete${NC}"
fi

if [ -f "backend/app/contexts/hrms/routes/leave_route.py" ] && \
   [ -f "frontend/src/pages/hr/leaves/index.vue" ]; then
    echo -e "${GREEN}✓ Leave Management: Ready${NC}"
else
    echo -e "${RED}✗ Leave Management: Incomplete${NC}"
fi

if [ -f "backend/app/contexts/hrms/routes/working_schedule_route.py" ]; then
    echo -e "${YELLOW}⚠ Working Schedule: Backend Ready, Frontend Pending${NC}"
else
    echo -e "${RED}✗ Working Schedule: Not Ready${NC}"
fi

if [ -f "backend/app/contexts/hrms/routes/work_location_route.py" ]; then
    echo -e "${YELLOW}⚠ Work Location: Backend Ready, Frontend Pending${NC}"
else
    echo -e "${RED}✗ Work Location: Not Ready${NC}"
fi

if [ -f "backend/app/contexts/hrms/routes/public_holiday_route.py" ]; then
    echo -e "${YELLOW}⚠ Public Holiday: Backend Ready, Frontend Pending${NC}"
else
    echo -e "${RED}✗ Public Holiday: Not Ready${NC}"
fi

if [ -f "backend/app/contexts/hrms/routes/deduction_rule_route.py" ]; then
    echo -e "${YELLOW}⚠ Deduction Rule: Backend Ready, Frontend Pending${NC}"
else
    echo -e "${RED}✗ Deduction Rule: Not Ready${NC}"
fi

echo ""
echo "=============================="
echo ""

# 6. Quick Start Commands
echo "🚀 Quick Start Commands"
echo "=============================="
echo ""
echo "Start Backend:"
echo "  cd backend && docker-compose up -d"
echo ""
echo "Start Frontend:"
echo "  cd frontend && pnpm install && pnpm dev"
echo ""
echo "Access System:"
echo "  Frontend: http://localhost:3000/hr"
echo "  Backend API: http://localhost:5001"
echo "  MongoDB Express: http://localhost:8081"
echo ""
echo "Default Login:"
echo "  Email: admin@school.com"
echo "  Password: admin123"
echo ""
echo "=============================="
echo ""
echo "✅ Verification Complete!"
echo ""
