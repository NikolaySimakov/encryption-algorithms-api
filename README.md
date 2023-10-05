# Encryption algorithms API

# Router

Description of router methods:

### `/encrypt/`

Encryption methods:

- `/encrypt/rsa` - implementation of RSA algorithm
- `/encrypt/aes` - implementation of AES algorithm
- `/encrypt/kuznechik` - implementation of Kuznechik algorithm
- `/encrypt/magma` - implementation of Magma algorithm

Accepts json in format:

```json
{
    key: "some key",
    body: "some body"
}
```

Returns JSON as response (example for aes algorithm):

```json
{
    body: "\\x98\\xd1(\\xdb\\x02\\x16\\x0f\\x05\\x11\\x1af\\xf5\\xe1\\xeb\\x8f6\\x8b/\\x08>l\\xbe;\"m[\\xf3v\\x1a\\xc1\\xe2\\xc6"
}
```

### `/decrypt/`

Decryption methods:

- `/json/message/` - method for searching encryption algorithm.

Accepts json in format:

```json
{
    key: "some key",
    body: "some body"
}
```

Returns:

```json
{
    info: "some info"
}