# app/services/api_clients/imobiliare_client.py
import requests
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom

logger = logging.getLogger(__name__)

class ImobiliareApiClient:
    """Client for the ImobiliareRO SOAP API that attempts to use public endpoints"""
    
    def __init__(self, endpoint_url="https://apiws.imobiliare.ro/index.php"):
        self.endpoint_url = endpoint_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'text/xml;charset=UTF-8',
            'SOAPAction': ''
        })
        self.session_id = None
    
    def get_apartments(self):
        """Get apartment listings using update_apartamente without authentication"""
        try:
            # Construct SOAP envelope for update_apartamente without sid
            soap_envelope = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope 
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:ns1="urn:api"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Body>
                    <ns1:update_apartamente>
                    </ns1:update_apartamente>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            
            # Send request
            logger.info(f"Sending update_apartamente request without authentication")
            response = self.session.post(self.endpoint_url, data=soap_envelope)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {self._pretty_xml(response.text)}")
            
            if response.status_code != 200:
                logger.error(f"Failed with status code: {response.status_code}")
                return []
            
            # Process the response even if it's an error to see what we get
            return self._try_parse_apartments(response.text)
            
        except Exception as e:
            logger.error(f"Error in get_apartments: {e}")
            return []
    
    def get_offers(self):
        """Get offers using obtine_oferte without authentication"""
        try:
            # Construct SOAP envelope for obtine_oferte
            soap_envelope = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope 
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:ns1="urn:api"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Body>
                    <ns1:obtine_oferte>
                    </ns1:obtine_oferte>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            
            # Send request
            logger.info(f"Sending obtine_oferte request without authentication")
            response = self.session.post(self.endpoint_url, data=soap_envelope)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {self._pretty_xml(response.text)}")
            
            if response.status_code != 200:
                logger.error(f"Failed with status code: {response.status_code}")
                return []
            
            # Process the response
            return self._try_parse_offers(response.text)
            
        except Exception as e:
            logger.error(f"Error in get_offers: {e}")
            return []
    
    def get_all_offers(self):
        """Get all offers using obtine_oferte_all without authentication"""
        try:
            # Construct SOAP envelope for obtine_oferte_all
            soap_envelope = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope 
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:ns1="urn:api"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Body>
                    <ns1:obtine_oferte_all>
                    </ns1:obtine_oferte_all>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            
            # Send request
            logger.info(f"Sending obtine_oferte_all request without authentication")
            response = self.session.post(self.endpoint_url, data=soap_envelope)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {self._pretty_xml(response.text)}")
            
            if response.status_code != 200:
                logger.error(f"Failed with status code: {response.status_code}")
                return []
            
            # Process the response
            return self._try_parse_all_offers(response.text)
            
        except Exception as e:
            logger.error(f"Error in get_all_offers: {e}")
            return []
    
    def get_version(self):
        """Get API version using setare_versiune without authentication"""
        try:
            # Construct SOAP envelope for setare_versiune
            soap_envelope = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope 
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:ns1="urn:api"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Body>
                    <ns1:setare_versiune>
                    </ns1:setare_versiune>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            
            # Send request
            logger.info(f"Sending setare_versiune request without authentication")
            response = self.session.post(self.endpoint_url, data=soap_envelope)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {self._pretty_xml(response.text)}")
            
            # Extract version info if available
            try:
                root = ET.fromstring(response.text)
                version_elements = root.findall('.//*versiune')
                if version_elements and len(version_elements) > 0:
                    return version_elements[0].text
                else:
                    return "Version information not available"
            except Exception as e:
                logger.error(f"Error parsing version response: {e}")
                return "Error parsing version information"
            
        except Exception as e:
            logger.error(f"Error in get_version: {e}")
            return "Error retrieving version information"
    
    def _try_parse_apartments(self, xml_text):
        """Attempt to parse apartments from XML, handling various possible formats"""
        apartments = []
        try:
            root = ET.fromstring(xml_text)
            
            # Try different possible element names and paths
            apartment_elements = []
            possible_paths = [
                './/*apartament', 
                './/*Apartament', 
                './/*apartamente',
                './/*Apartamente',
                './/*return//*apartament',
                './/*return//*Apartament'
            ]
            
            for path in possible_paths:
                elems = root.findall(path)
                if elems:
                    logger.info(f"Found {len(elems)} elements using path: {path}")
                    apartment_elements.extend(elems)
            
            # Process each apartment element
            for apt_elem in apartment_elements:
                try:
                    apartment = self._extract_property_data(apt_elem, "apartment")
                    if apartment:
                        apartments.append(apartment)
                except Exception as e:
                    logger.error(f"Error processing apartment element: {e}")
            
            # If we found fault elements instead of apartments
            if not apartments:
                fault_elements = root.findall('.//*Fault') or root.findall('.//*fault')
                if fault_elements:
                    for fault in fault_elements:
                        fault_string = fault.find('.//*faultstring')
                        if fault_string is not None:
                            logger.error(f"SOAP Fault: {fault_string.text}")
            
            return apartments
            
        except Exception as e:
            logger.error(f"Error parsing apartments XML: {e}")
            return []
    
    def _try_parse_offers(self, xml_text):
        """Attempt to parse offers from XML"""
        offers = []
        try:
            root = ET.fromstring(xml_text)
            
            # Try different possible paths for offers
            offer_elements = []
            possible_paths = [
                './/*oferta', 
                './/*Oferta', 
                './/*oferte',
                './/*Oferte',
                './/*return//*oferta',
                './/*return//*Oferta'
            ]
            
            for path in possible_paths:
                elems = root.findall(path)
                if elems:
                    logger.info(f"Found {len(elems)} elements using path: {path}")
                    offer_elements.extend(elems)
            
            # Process each offer element
            for offer_elem in offer_elements:
                try:
                    offer = self._extract_property_data(offer_elem, "offer")
                    if offer:
                        offers.append(offer)
                except Exception as e:
                    logger.error(f"Error processing offer element: {e}")
            
            return offers
            
        except Exception as e:
            logger.error(f"Error parsing offers XML: {e}")
            return []
    
    def _try_parse_all_offers(self, xml_text):
        """Attempt to parse all offers from XML"""
        all_offers = []
        try:
            root = ET.fromstring(xml_text)
            
            # Try to find and process apartments
            apartments = self._try_parse_apartments(xml_text)
            if apartments:
                all_offers.extend(apartments)
            
            # Try to find houses
            house_elements = []
            house_paths = [
                './/*casa', 
                './/*Casa', 
                './/*case',
                './/*Case',
                './/*return//*casa',
                './/*return//*Casa'
            ]
            
            for path in house_paths:
                elems = root.findall(path)
                if elems:
                    logger.info(f"Found {len(elems)} house elements using path: {path}")
                    house_elements.extend(elems)
            
            # Process houses
            for house_elem in house_elements:
                try:
                    house = self._extract_property_data(house_elem, "house")
                    if house:
                        all_offers.append(house)
                except Exception as e:
                    logger.error(f"Error processing house element: {e}")
            
            # Try to find land listings
            land_elements = []
            land_paths = [
                './/*teren', 
                './/*Teren', 
                './/*terenuri',
                './/*Terenuri',
                './/*return//*teren',
                './/*return//*Teren'
            ]
            
            for path in land_paths:
                elems = root.findall(path)
                if elems:
                    logger.info(f"Found {len(elems)} land elements using path: {path}")
                    land_elements.extend(elems)
            
            # Process lands
            for land_elem in land_elements:
                try:
                    land = self._extract_property_data(land_elem, "land")
                    if land:
                        all_offers.append(land)
                except Exception as e:
                    logger.error(f"Error processing land element: {e}")
            
            return all_offers
            
        except Exception as e:
            logger.error(f"Error parsing all offers XML: {e}")
            return []
    
    def _extract_property_data(self, elem, property_type):
        """Extract property data from an XML element"""
        property_data = {
            "source": "imobiliare.ro",
            "features": {},
            "images": []
        }
        
        # List of all child elements for debugging
        child_tags = [child.tag.split('}')[-1] for child in elem]
        logger.debug(f"Child elements of {property_type}: {child_tags}")
        
        # Process all child elements
        for child in elem:
            tag = child.tag.split('}')[-1]  # Remove namespace prefix if present
            
            # Handle different fields
            if tag == 'id':
                property_data['external_id'] = child.text
            elif tag == 'titlu':
                property_data['title'] = child.text
            elif tag == 'descriere':
                property_data['description'] = child.text
            elif tag == 'pret':
                try:
                    property_data['price'] = float(child.text)
                except (ValueError, TypeError):
                    property_data['price'] = 0
            elif tag == 'moneda':
                property_data['currency'] = child.text
            elif tag == 'oras':
                city = child.text or ""
                property_data['location'] = city
            elif tag == 'zona':
                zone = child.text or ""
                if 'location' in property_data:
                    property_data['location'] = f"{property_data['location']}, {zone}"
                else:
                    property_data['location'] = zone
            elif tag in ['suprafata', 'suprafata_utila']:
                try:
                    property_data['area'] = float(child.text)
                except (ValueError, TypeError):
                    property_data['area'] = 0
            elif tag == 'camere':
                try:
                    property_data['rooms'] = int(child.text)
                except (ValueError, TypeError):
                    property_data['rooms'] = 0
            elif tag == 'poze':
                # Process images
                for img_elem in child:
                    if img_elem.tag.endswith('poza'):
                        url = None
                        for img_child in img_elem:
                            if img_child.tag.endswith('url'):
                                url = img_child.text
                                break
                        if url:
                            property_data['images'].append({
                                "url": url,
                                "local_path": ""
                            })
            else:
                # Add other fields to features
                if child.text and child.text.strip():
                    property_data['features'][tag] = child.text
        
        # Set defaults for missing required fields
        if 'external_id' not in property_data:
            property_data['external_id'] = f"imobiliare-{property_type}-{id(elem)}"
        if 'title' not in property_data:
            property_data['title'] = f"{property_type.capitalize()} Listing"
        if 'description' not in property_data:
            property_data['description'] = ""
        if 'price' not in property_data:
            property_data['price'] = 0
        if 'currency' not in property_data:
            property_data['currency'] = "EUR"
        if 'location' not in property_data:
            property_data['location'] = ""
        if 'area' not in property_data:
            property_data['area'] = 0
        if 'rooms' not in property_data:
            property_data['rooms'] = 0
        
        return property_data
    
    def _pretty_xml(self, xml_str):
        """Format XML string for pretty printing"""
        try:
            parsed = xml.dom.minidom.parseString(xml_str)
            return parsed.toprettyxml(indent="  ")
        except Exception:
            return xml_str