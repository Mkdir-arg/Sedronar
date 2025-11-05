#!/usr/bin/env python3
"""
Test simple para verificar WebSockets funcionando
"""
import asyncio
import websockets
import json

async def test_websocket():
    """Test básico de conexión WebSocket"""
    try:
        # Conectar al WebSocket
        uri = "ws://localhost:9000/ws/conversaciones/"
        print(f"Conectando a {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("Conexion WebSocket establecida!")
            
            # Enviar mensaje de prueba
            test_message = {
                "type": "test",
                "message": "Hola desde test"
            }
            
            await websocket.send(json.dumps(test_message))
            print("Mensaje enviado")
            
            # Esperar respuesta (con timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Respuesta recibida: {response}")
            except asyncio.TimeoutError:
                print("Timeout - sin respuesta (normal para test sin auth)")
            
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Conexion cerrada (normal sin autenticacion): {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Probando WebSockets...")
    asyncio.run(test_websocket())
    print("Test completado")