# DDNS Client for ASUS Merlin Router

### Features

- CloudFlare Support

### Getting Started

Clone this repository

```shell
git clone https://github.com/YanzheL/ddnscli.git
```

Copy the project directory to your router's jffs partition

```shell
cp -r ddnscli /jffs/
```

Create ddns-start script as `/jffs/scripts/ddns-start`

```
#!/bin/sh
/jffs/ddnscli/ddnsmgr.py $1
/sbin/ddns_custom_updated $(($?==0))
```

Grant execution permission

```shell
chmod +x /jffs/scripts/ddns-start
```

Create credentials file `credentials.py` under project root directory, and fill in required information of your cloudflare API key.

`/jffs/ddnscli/credentials.py`

```python
CLOUDFLARE_CREDENTIAL = {
    'api_key': {
        'email': 'YOUR_CLOUDFLARE_EMAIL',
        'token': 'YOUR_CLOUDFLARE_TOKEN'
    },
    'zone_id': 'YOUR_CLOUDFLARE_ZONE_ID',
    'domain_name': 'YOUR_DOMAIN'
}
```

Have fun!
