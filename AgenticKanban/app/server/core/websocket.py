from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any
import json
import asyncio
import logging
from datetime import datetime

# Global connection manager
connection_manager = None

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""

    def __init__(self):
        # Dictionary mapping adw_id to set of websockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Global connections (listening to all updates)
        self.global_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, adw_id: str = None):
        """Accept a WebSocket connection"""
        await websocket.accept()

        if adw_id:
            # Connection for specific workflow
            if adw_id not in self.active_connections:
                self.active_connections[adw_id] = set()
            self.active_connections[adw_id].add(websocket)
            logging.info(f"WebSocket connected for workflow: {adw_id}")
        else:
            # Global connection
            self.global_connections.add(websocket)
            logging.info("Global WebSocket connection established")

    def disconnect(self, websocket: WebSocket, adw_id: str = None):
        """Remove a WebSocket connection"""
        if adw_id and adw_id in self.active_connections:
            self.active_connections[adw_id].discard(websocket)
            if not self.active_connections[adw_id]:
                del self.active_connections[adw_id]
            logging.info(f"WebSocket disconnected for workflow: {adw_id}")
        else:
            self.global_connections.discard(websocket)
            logging.info("Global WebSocket connection closed")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logging.error(f"Error sending WebSocket message: {e}")

    async def broadcast_to_workflow(self, adw_id: str, message: Dict[str, Any]):
        """Send message to all connections listening to a specific workflow"""
        message["timestamp"] = datetime.utcnow().isoformat()

        if adw_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[adw_id]:
                try:
                    await connection.send_text(json.dumps(message, default=str))
                except Exception as e:
                    logging.error(f"Error broadcasting to workflow {adw_id}: {e}")
                    disconnected.add(connection)

            # Remove disconnected connections
            for connection in disconnected:
                self.active_connections[adw_id].discard(connection)

        # Also send to global connections
        await self.broadcast_global(message)

    async def broadcast_global(self, message: Dict[str, Any]):
        """Send message to all global connections"""
        message["timestamp"] = datetime.utcnow().isoformat()

        disconnected = set()
        for connection in self.global_connections:
            try:
                await connection.send_text(json.dumps(message, default=str))
            except Exception as e:
                logging.error(f"Error broadcasting globally: {e}")
                disconnected.add(connection)

        # Remove disconnected connections
        for connection in disconnected:
            self.global_connections.discard(connection)

    def get_connection_count(self, adw_id: str = None) -> int:
        """Get the number of active connections"""
        if adw_id:
            return len(self.active_connections.get(adw_id, set()))
        return len(self.global_connections)

    def get_all_connection_counts(self) -> Dict[str, int]:
        """Get connection counts for all workflows"""
        counts = {adw_id: len(connections) for adw_id, connections in self.active_connections.items()}
        counts["global"] = len(self.global_connections)
        return counts


# Initialize global connection manager
def get_connection_manager() -> ConnectionManager:
    """Get or create the global connection manager"""
    global connection_manager
    if connection_manager is None:
        connection_manager = ConnectionManager()
    return connection_manager


async def websocket_endpoint(websocket: WebSocket, adw_id: str):
    """WebSocket endpoint for workflow updates"""
    manager = get_connection_manager()
    await manager.connect(websocket, adw_id)

    try:
        # Send initial connection confirmation
        await manager.send_personal_message({
            "type": "connection_established",
            "adw_id": adw_id,
            "message": f"Connected to workflow {adw_id}"
        }, websocket)

        # Keep connection alive and handle messages
        while True:
            try:
                # Receive message from client (for ping/pong or other client messages)
                data = await websocket.receive_text()
                message = json.loads(data)

                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logging.error(f"Error in WebSocket message handling: {e}")
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logging.error(f"WebSocket error for {adw_id}: {e}")
    finally:
        manager.disconnect(websocket, adw_id)


async def global_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for global updates (all workflows)"""
    manager = get_connection_manager()
    await manager.connect(websocket)

    try:
        # Send initial connection confirmation
        await manager.send_personal_message({
            "type": "global_connection_established",
            "message": "Connected to global workflow updates"
        }, websocket)

        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)

                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logging.error(f"Error in global WebSocket message handling: {e}")
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logging.error(f"Global WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)


async def notify_workflow_update(adw_id: str, message: Dict[str, Any]):
    """Utility function to send updates to WebSocket subscribers"""
    manager = get_connection_manager()
    await manager.broadcast_to_workflow(adw_id, message)


async def notify_global_update(message: Dict[str, Any]):
    """Utility function to send global updates to all subscribers"""
    manager = get_connection_manager()
    await manager.broadcast_global(message)


# Health check for WebSocket connections
async def get_websocket_stats() -> Dict[str, Any]:
    """Get WebSocket connection statistics"""
    manager = get_connection_manager()
    return {
        "connection_counts": manager.get_all_connection_counts(),
        "active_workflows": list(manager.active_connections.keys()),
        "global_connections": len(manager.global_connections),
        "total_workflow_connections": sum(len(connections) for connections in manager.active_connections.values())
    }