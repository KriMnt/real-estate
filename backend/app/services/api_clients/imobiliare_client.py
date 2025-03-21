# app/services/api_clients/imobiliare_client.py
import zeep
import logging
from zeep.exceptions import TransportError

logger = logging.getLogger(__name__)

class ImobiliareApiClient:
    """Client for the ImobiliareRO SOAP API"""
    
    def __init__(self, wsdl_url="https://apiws.imobiliare.ro?wsdl"):
        self.wsdl_url = wsdl_url
        self.client = zeep.Client(wsdl_url)
        self.session_id = None
    
    def login(self, username, password, ip="127.0.0.1", env="prod"):
        """Login to the API and get session ID"""
        try:
            # Structure the input according to WSDL
            login_input = {
                'id': username,
                'parola': password,
                'ip': ip,
                'env': env
            }
            
            result = self.client.service.login(**login_input)
            
            # Debug the result structure
            logger.info(f"Login result: {result}")
            
            # Extract session ID based on response structure
            if hasattr(result, 'sid'):
                self.session_id = result.sid
                logger.info(f"Login successful. Session ID: {self.session_id}")
                return True
            else:
                logger.error(f"Login failed: No session ID returned")
                return False
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def get_apartments(self):
        """Get apartment listings using update_apartamente"""
        if not self.session_id:
            logger.error("Not logged in, cannot get apartments")
            return []
            
        try:
            # Structure the input according to WSDL
            input_data = {
                'sid': self.session_id
            }
            
            result = self.client.service.update_apartamente(**input_data)
            
            # Debug the result structure
            logger.info(f"Apartments result structure: {result}")
            
            # Process results
            properties = []
            
            # This part will need adjustment based on the actual response structure
            if hasattr(result, 'apartamente') and result.apartamente:
                for apt in result.apartamente:
                    try:
                        property_data = self._convert_to_property_model(apt, "apartment")
                        properties.append(property_data)
                    except Exception as e:
                        logger.error(f"Error processing apartment: {e}")
                        continue
            
            return properties
        except Exception as e:
            logger.error(f"Error fetching apartments: {e}")
            return []
    
    def get_houses(self):
        """Get house listings using update_casevile"""
        if not self.session_id:
            logger.error("Not logged in, cannot get houses")
            return []
            
        try:
            # Structure the input according to WSDL
            input_data = {
                'sid': self.session_id
            }
            
            result = self.client.service.update_casevile(**input_data)
            
            # Debug the result structure
            logger.info(f"Houses result structure: {result}")
            
            # Process results
            properties = []
            
            # This part will need adjustment based on the actual response structure
            if hasattr(result, 'case') and result.case:
                for house in result.case:
                    try:
                        property_data = self._convert_to_property_model(house, "house")
                        properties.append(property_data)
                    except Exception as e:
                        logger.error(f"Error processing house: {e}")
                        continue
            
            return properties
        except Exception as e:
            logger.error(f"Error fetching houses: {e}")
            return []
    
    def _convert_to_property_model(self, api_property, property_type):
        """Convert API property object to our property model"""
        try:
            # Log the entire property to see its structure
            logger.info(f"Converting property: {api_property}")
            
            # Base features dictionary
            features = {}
            
            # Extract common fields
            property_id = getattr(api_property, 'id', '')
            title = getattr(api_property, 'titlu', f"{property_type.capitalize()}")
            description = getattr(api_property, 'descriere', "")
            price = float(getattr(api_property, 'pret', 0))
            currency = getattr(api_property, 'moneda', "EUR")
            
            # Location
            city = getattr(api_property, 'oras', '')
            zone = getattr(api_property, 'zona', '')
            location = f"{city}, {zone}" if zone else city
            
            # Property-specific fields
            area = 0
            rooms = 0
            
            if property_type == "apartment":
                rooms = int(getattr(api_property, 'camere', 0))
                area = float(getattr(api_property, 'suprafata', 0))
            elif property_type == "house":
                rooms = int(getattr(api_property, 'camere', 0))
                area = float(getattr(api_property, 'suprafata_utila', 0))
            
            # Create property object
            property_data = {
                "external_id": str(property_id),
                "source": "imobiliare.ro",
                "title": title,
                "description": description,
                "price": price,
                "currency": currency,
                "location": location,
                "area": area,
                "rooms": rooms,
                "features": features,
                "images": []  # We'll handle images later
            }
            
            return property_data
        except Exception as e:
            logger.error(f"Error converting property: {e}")
            raise