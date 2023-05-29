import libvirt


def create_vm():
    conn = libvirt.open()  # Ouvrir une connexion avec l'hyperviseur

    # Spécifier les paramètres de la machine virtuelle
    vm_name = "MaMachineVirtuelle"
    vm_memory = 2048  # Mémoire en Mo
    vm_vcpu = 2  # Nombre de vCPU
    vm_disk_path = "/chemin/vers/mon_image.qcow2"
    vm_disk_size = 10 * 1024 * 1024 * 1024  # Taille du disque en octets (10 Go)
    vm_network = "br0"  # Interface réseau

    # Créer la configuration de la machine virtuelle
    xml_config = f'''
        <domain type='kvm'>
            <name>{vm_name}</name>
            <memory unit='KiB'>{vm_memory * 1024}</memory>
            <vcpu placement='static'>{vm_vcpu}</vcpu>
            <devices>
                <disk type='file' device='disk'>
                    <driver name='qemu' type='qcow2'/>
                    <source file='{vm_disk_path}'/>
                    <target dev='vda' bus='virtio'/>
                </disk>
                <interface type='bridge'>
                    <mac address='52:54:00:01:23:45'/>
                    <source bridge='{vm_network}'/>
                    <model type='virtio'/>
                </interface>
            </devices>
        </domain>
    '''

    # Créer la machine virtuelle
    vm = conn.createXML(xml_config, 0)

    if vm is not None:
        print("Machine virtuelle créée avec succès.")

        # Démarrer la machine virtuelle
        vm.create()
    else:
        print("Échec de la création de la machine virtuelle.")

    conn.close()  # Fermer la connexion avec l'hyperviseur


create_vm()
