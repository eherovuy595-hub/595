import docker
import sys
from typing import List, Dict

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def list_containers(self) -> List[Dict]:
        containers = self.client.containers.list(all=True)
        result = []
        for container in containers:
            result.append({
                'id': container.id[:12],
                'name': container.name,
                'status': container.status,
                'image': container.image.tags
            })
        return result
    
    def create_container(self, image: str, name: str, command: str = None) -> Dict:
        try:
            container = self.client.containers.create(image, command=command, name=name)
            return {'success': True, 'container_id': container.id, 'name': name}
        except docker.errors.ImageNotFound:
            return {'success': False, 'error': f'Image {image} not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def start_container(self, container_id: str) -> Dict:
        try:
            container = self.client.containers.get(container_id)
            container.start()
            return {'success': True, 'message': f'Container {container_id} started'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def stop_container(self, container_id: str) -> Dict:
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            return {'success': True, 'message': f'Container {container_id} stopped'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def remove_container(self, container_id: str, force: bool = False) -> Dict:
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            return {'success': True, 'message': f'Container {container_id} removed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_container_logs(self, container_id: str) -> str:
        try:
            container = self.client.containers.get(container_id)
            return container.logs(decode=True)
        except Exception as e:
            return f'Error: {str(e)}'

def main():
    manager = DockerManager()
    
    print('=== Docker Container Manager ===')
    print('Listing all containers:')
    containers = manager.list_containers()
    for container in containers:
        print(f"  - {container['name']}: {container['status']}")

if __name__ == '__main__':
    main()