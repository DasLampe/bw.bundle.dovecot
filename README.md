# Dovecot via Bundlewrap
Install Dovecot via Bundlewrap.


Config based on [Mailserver mit Dovecot, Postfix, MySQL und Rspamd unter Debian 9 Stretch](https://thomas-leister.de/mailserver-debian-stretch/)


## Config
```python
'dovecot': {
    'postmaster': 'postmaster@example.org',
    'ssl_cert': '/etc/letsencrypt/live/example.org/fullchain.pem',
    'ssl_key': '/etc/letsencrypt/live/example.org/privkey.pem',
    'default_passscheme': 'SHA512-CRYPT',
},

# See dependencies
'postfix': {
    'database': {
        'host': 'localhost',
        'mysql_user': 'vmail_bw',
        'password': 'mysql_vmail_user_example.org',
        'db': 'vmail_bw',
    }
}
```

## Dependencies
- [postfix via Bundlewrap](https://github.com/DasLampe/bw.bundle.postfix), it's possible to run dovecot without but make no sense

## Suggestions
- [rspamd via bundlewrap](https://github.com/DasLampe/bw.bundle.rspamd)
