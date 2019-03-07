global repo
global node

@metadata_processor
def add_iptables(metadata):
    if node.has_bundle("iptables"):
        metadata += repo.libs.iptables.accept().chain('INPUT').dest_port('993').protocol('tcp')
        metadata += repo.libs.iptables.accept().chain('INPUT').dest_port('143').protocol('tcp')
    return metadata, DONE
