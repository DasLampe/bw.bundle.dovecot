global node, repo

config = node.metadata.get('dovecot', {})

svc_systemd = {
    'dovecot': {
        'enabled': True,
        'running': True,
        'needs': [
            'pkg_apt:',
            'file:/etc/dovecot/dovecot.conf',
        ],
    }
}

directories = {
    f'{config.get("mail_dir")}/sieve/global': {
        'owner': config.get('mail_user'),
        'group': config.get('mail_group'),
        'mode': '0770',
    }
}

files = {
    '/etc/dovecot/dovecot.conf': {
        'source': 'etc/dovecot/dovecot.conf',
        'content_type': 'mako',
        'context': {
            'cfg': config,
            'postmaster': config.get('postmaster'),
            'ssl_cert': config.get('ssl_cert'),
            'ssl_key': config.get('ssl_key'),
        },
        'owner': config.get('user'),
        'group': config.get('group'),
        'triggers': [
            'svc_systemd:dovecot:restart',
        ],
        'needs': {
            'pkg_apt:dovecot-core',
        }
    },

    '/etc/dovecot/dovecot-sql.conf': {
        'source': 'etc/dovecot/dovecot-sql.conf',
        'content_type': 'mako',
        'context': {
            'mysql_host': config.get('database').get('host'),
            'mysql_user': config.get('database').get('user'),
            'mysql_password': config.get('database').get('password'),
            'mysql_db':  config.get('database').get('db'),
            'default_passscheme': config.get('default_passscheme'),
        },
        'owner': config.get('user'),
        'group': config.get('group'),
        'mode': '0440',
    }
}

for file in ['spam-global.sieve', 'learn-spam.sieve', 'learn-ham.sieve']:
    files[f'{config.get("mail_dir")}/sieve/global/{file}'] = {
        'source': f'var/vmail/sieve/global/{file}',
        'owner': config.get('mail_user'),
        'group': config.get('mail_group'),
    }
