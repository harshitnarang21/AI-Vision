#!/bin/bash

# Self-signed SSL Certificate Setup

echo "🔐 Setting up self-signed SSL certificate..."
echo ""

# Check if openssl is installed
if ! command -v openssl &> /dev/null; then
    echo "❌ openssl is not installed"
    echo "Please install openssl first"
    exit 1
fi

echo "Generating self-signed certificate..."
echo ""

# Generate certificate
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem \
    -keyout key.pem \
    -days 365 \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=192.168.1.45"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Certificate generated successfully!"
    echo ""
    echo "Files created:"
    echo "  - cert.pem (certificate)"
    echo "  - key.pem (private key)"
    echo ""
    echo "⚠️  Note: You'll need to accept the security warning in your browser"
    echo "   (this is normal for self-signed certificates)"
    echo ""
    echo "Next steps:"
    echo "1. Update app.py to use SSL (see instructions below)"
    echo "2. Restart the app"
    echo "3. Access via: https://192.168.1.45:5001/"
    echo ""
    echo "To update app.py, change the last line to:"
    echo "  app.run(host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'), debug=config.Config.DEBUG)"
else
    echo "❌ Failed to generate certificate"
    exit 1
fi


