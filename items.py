global node, repo

mysql_user = node.metadata.get('postfix', {}).get('database', {}).get('user', 'vmail_bw')
mysql_password = node.metadata.get('postfix', {}).get('database', {}). \
    get('password', repo.vault.password_for("mysql_{}_user_{}".format(mysql_user, node.name)))
mysql_host = node.metadata.get('postfix', {}).get('database', {}).get('host', '127.0.0.1')
mysql_db = node.metadata.get('postfix', {}).get('database', {}).get('db', 'vmail_bw')


pkg = {
    'dovecot-core': {},
    'dovecot-imapd': {},
    'dovecot-lmtpd': {},
    'dovecot-mysql': {},
    'dovecot-sieve': {},
}

directories = {}
files = {}

####
# Clean up
####
directories['/etc/dovecot'] = {
    'purge': True,
}


####
# Create Config
####
config = node.metadata.get('dovecot', {})

files['/etc/dovecot/dovecot.conf'] = {
    'source': 'etc/dovecot/dovecot.conf',
    'content_type': 'mako',
    'context': {
        'postmaster': config.get('postmaster', 'postmaster@{}'.format(node.hostname)),
        'ssl_cert': config.get('ssl_cert', '/etc/letsencrypt/live/{}/fullchain.pem'.format(node.hostname)),
        'ssl_key': config.get('ssl_key', '/etc/letsencrypt/live/{}/privkey.pem'.format(node.hostname)),
    },
    'owner': 'dovecot',
    'group': 'dovecot',
}

files['/etc/dovecot/dovecot-sql.conf'] = {
    'source': 'etc/dovecot/dovecot-sql.conf',
    'content_type': 'mako',
    'context': {
        'mysql_host': mysql_host,
        'mysql_user': mysql_user,
        'mysql_password': mysql_password,
        'mysql_db':  mysql_db,
        'default_passscheme': config.get('default_passscheme', 'SHA512-CRYPT'),
    },
    'owner': 'dovecot',
    'group': 'dovecot',
    'mode': '0440',
}

####
# Sieve rules
####
directories['/var/vmail/sieve/global'] = {
    'owner': 'vmail',
    'group': 'vmail',
    'mode': '0770',
}

for file in ['spam-global.sieve', 'learn-spam.sieve', 'learn-ham.sieve']:
    files['/var/vmail/sieve/global/{}'.format(file)] = {
        'source': 'var/vmail/sieve/global/{}'.format(file),
        'owner': 'vmail',
        'group': 'vmail',
    }
