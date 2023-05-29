import asyncio
import socket

async def scan_port(target, port):
    try:
        # Création d'un objet socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Délai d'attente pour la connexion

        # Tentative de connexion au port
        result = await loop.sock_connect(sock, (target, port))

        if result == 0:
            print(f"Port {port}: Open")

        # Fermeture de la connexion
        sock.close()

    except KeyboardInterrupt:
        print("\nScanning interrupted by user.")
        return

    except socket.gaierror:
        print("Hostname could not be resolved.")
        return

    except socket.error:
        print("Could not connect to the server.")
        return


async def scan_ports(target, start_port, end_port):
    print(f"Scanning ports on {target}...")

    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(scan_port(target, port))

    await asyncio.gather(*tasks)

    print("Port scanning complete.")


# Exemple d'utilisation
target_host = "localhost"  # Remplacez par l'adresse IP ou le nom de domaine cible
start_port = 1
end_port = 100

loop = asyncio.get_event_loop()
loop.run_until_complete(scan_ports(target_host, start_port, end_port))
