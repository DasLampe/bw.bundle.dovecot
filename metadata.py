global repo
global node

defaults = {
    'dovecot': {
        'user': 'dovecot',
        'group': 'dovecot',
        'postmaster': f'postmaster@{node.hostname}',

        'ssl_cert': f'/etc/letsencrypt/live/{node.hostname}/fullchain.pem',
        'ssl_key': f'/etc/letsencrypt/live/{node.hostname}/privkey.pem',

        'default_passscheme': 'SHA512-CRYPT',

        'postfix_user': 'postfix',
        'postfix_group': 'postfix',

        'mail_user': 'vmail',
        'mail_group': 'vmail',
        'mail_dir': '/var/vmail',

        'port_imap': 143,
        'port_imaps': 993,
        'port_sieve': 4190,

        'database': {
            'user': 'vmail_bw',
            'password': repo.vault.password_for("mysql_{}_user_{}".format('vmail_bw', node.name)),
            'host': 'localhost',
            'db': 'vmail_bw',
        }
    },
    'apt': {
        'packages': {
            'dovecot-core': {},
            'dovecot-imapd': {},
            'dovecot-lmtpd': {},
            'dovecot-mysql': {},
            'dovecot-sieve': {},
            'dovecot-managesieved': {},
        }
    }
}

@metadata_reactor
def add_iptables(metadata):
    meta_tables = {}
    if node.has_bundle("iptables"):
        meta_tables += repo.libs.iptables.accept().chain('INPUT').dest_port('993').protocol('tcp')
        meta_tables += repo.libs.iptables.accept().chain('INPUT').dest_port('143').protocol('tcp')
    return meta_tables
