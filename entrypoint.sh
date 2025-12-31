#!/bin/sh

# Ensure database migrations are applied
echo "Applying database migrations..."
python manage.py migrate --noinput

# Print the requested banner
echo ""
echo "=============================================="
echo "   SMART CLASS COMPANION IS READY!"
echo "=============================================="
echo ""
echo "   Web App:  http://localhost:8000"
echo ""
echo "   Oracle Database Credentials:"
echo "   ----------------------------"
echo "   Host:     localhost (or 'oracle' from inside Docker)"
echo "   Port:     1521"
echo "   Service:  xepdb1"
echo "   User:     smartclass_user"
echo "   Password: smartclass_pass"
echo ""
echo "   Connection String:"
echo "   smartclass_user/smartclass_pass@localhost:1521/xepdb1"
echo ""
echo "=============================================="
echo ""

# Execute the main command
exec "$@"
