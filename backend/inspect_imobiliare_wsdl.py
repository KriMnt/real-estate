# inspect_imobiliare_wsdl.py
import logging
from zeep import Client
from zeep.wsdl.utils import etree_to_string
import xml.dom.minidom

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def inspect_wsdl():
    """Inspect the ImobiliareRO WSDL in detail"""
    try:
        wsdl_url = "https://apiws.imobiliare.ro?wsdl"
        client = Client(wsdl_url)
        
        # Print all available operations
        print("\n=== AVAILABLE OPERATIONS ===")
        for service in client.wsdl.services.values():
            print(f"Service: {service.name}")
            for port in service.ports.values():
                print(f"  Port: {port.name}")
                operations = port.binding._operations.values()
                for operation in operations:
                    print(f"    Operation: {operation.name}")
                    
                    # Input parameters
                    input_message = operation.input
                    if input_message:
                        print(f"      Input message: {input_message.name}")
                        if hasattr(input_message, 'body') and hasattr(input_message.body, 'parts'):
                            for name, part in input_message.body.parts.items():
                                print(f"        Parameter: {name} - Type: {part.element}")
        
        # Print available types
        print("\n=== TYPE INFORMATION ===")
        type_factory = client.type_factory('ns0')
        for item in dir(type_factory):
            if not item.startswith('_'):
                print(f"  Type: {item}")
        
        # Try creating a login request
        print("\n=== LOGIN REQUEST EXAMPLE ===")
        try:
            # First attempt: using factory to create request object
            login_request_type = getattr(type_factory, 'loginRequest', None)
            if login_request_type:
                login_request = login_request_type(id="test", parola="test", ip="127.0.0.1", env="test")
                xml = etree_to_string(client.create_message(client.service, 'login', login_request))
                pretty_xml = xml.dom.minidom.parseString(xml).toprettyxml()
                print(f"Sample login request XML:\n{pretty_xml}")
            else:
                print("loginRequest type not found, trying LoginRequest...")
                
                # Second attempt: try with different casing
                login_request_type = getattr(type_factory, 'LoginRequest', None)
                if login_request_type:
                    login_request = login_request_type(id="test", parola="test", ip="127.0.0.1", env="test")
                    xml = etree_to_string(client.create_message(client.service, 'login', login_request))
                    pretty_xml = xml.dom.minidom.parseString(xml).toprettyxml()
                    print(f"Sample login request XML:\n{pretty_xml}")
                else:
                    print("LoginRequest type not found, trying direct login...")
                    
                    # Third attempt: try without creating a specific request object
                    xml = etree_to_string(client.create_message(
                        client.service, 'login', id="test", parola="test", ip="127.0.0.1", env="test"
                    ))
                    pretty_xml = xml.dom.minidom.parseString(xml).toprettyxml()
                    print(f"Sample login request XML:\n{pretty_xml}")
        except Exception as e:
            print(f"Error creating login request: {e}")
            
            # Final attempt: try with a dictionary
            try:
                print("\nTrying with dictionary input...")
                xml = etree_to_string(client.create_message(
                    client.service, 'login', {'id': "test", 'parola': "test", 'ip': "127.0.0.1", 'env': "test"}
                ))
                pretty_xml = xml.dom.minidom.parseString(xml).toprettyxml()
                print(f"Sample login request XML:\n{pretty_xml}")
            except Exception as e:
                print(f"Error with dictionary input: {e}")
        
    except Exception as e:
        logger.error(f"Error inspecting WSDL: {e}")

if __name__ == "__main__":
    inspect_wsdl()