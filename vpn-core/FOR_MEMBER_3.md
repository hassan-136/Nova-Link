# Integration Guide for Member 3 (Security)

## Server Public Key

**Location:** `vpn-core/keys/server_public.key`

**View it:**
```cmd
type vpn-core\keys\server_public.key
```

**Your Key:**
[Paste your actual public key here after running the command above]

## API Endpoint
```
GET http://localhost:5000/api/server/info
```

Returns:
```json
{
  "server_public_key": "YOUR_KEY_HERE",
  "server_ip": "10.8.0.1",
  "server_port": 51820
}
```

## Integration Points

1. Use this public key for:
   - Certificate generation
   - Encryption setup
   - Client authentication

2. Current encryption:
   - Algorithm: X25519 (WireGuard standard)
   - Key format: Base64-encoded

3. Security testing:
   - Test against these API endpoints
   - Verify key exchange works
   - Check encryption implementation
   - 

## Questions?
Contact me: [Your contact info]
Get your actual server public key:
cmdcd vpn-core\keys
type server_public.key
Copy that key and paste it into the file above where it says "YOUR_KEY_HERE"
