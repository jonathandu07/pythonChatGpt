import asyncio


async def handle_client(reader, writer, destination_host, destination_port):
    # Établissement de la connexion avec la destination
    destination_reader, destination_writer = await asyncio.open_connection(destination_host, destination_port)

    async def forward(source, destination):
        try:
            while True:
                data = await source.read(1024)
                if not data:
                    break
                destination.write(data)
                await destination.drain()
        except asyncio.CancelledError:
            pass

    # Redirection des données entre le client et la destination
    client_to_destination = asyncio.create_task(forward(reader, destination_writer))
    destination_to_client = asyncio.create_task(forward(destination_reader, writer))

    try:
        await asyncio.gather(client_to_destination, destination_to_client)
    finally:
        # Fermeture des connexions
        writer.close()
        destination_writer.close()


async def start_proxy_server(proxy_port, destination_host, destination_port):
    server = await asyncio.start_server(
        lambda reader, writer: handle_client(reader, writer, destination_host, destination_port),
        '0.0.0.0', proxy_port)
    print(f"Proxy server started on port {proxy_port}")

    async with server:
        await server.serve_forever()


async def main():
    proxy_port = 8080  # Port du proxy
    destination_host = 'www.example.com'  # Hôte de destination
    destination_port = 80  # Port de destination

    await start_proxy_server(proxy_port, destination_host, destination_port)


asyncio.run(main())
