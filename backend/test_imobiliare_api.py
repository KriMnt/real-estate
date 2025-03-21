# test_imobiliare_api.py
import logging
from app.services.api_clients.imobiliare_client import ImobiliareApiClient
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api():
    """Test the ImobiliareRO API client"""
    client = ImobiliareApiClient()
    
    # Try anonymous access first (some SOAP APIs allow this for public data)
    logger.info("Testing apartments retrieval without login...")
    try:
        apartments = client.get_apartments()
        logger.info(f"Found {len(apartments)} apartments")
        
        # Print the first apartment if available
        if apartments:
            logger.info(f"First apartment: {json.dumps(apartments[0], indent=2)}")
    except Exception as e:
        logger.error(f"Error getting apartments without login: {e}")
    
    # Now try with login
    logger.info("\nTesting login...")
    login_successful = client.login(
        username="api_test",  # Test credentials - we'll need real ones eventually
        password="test_password"
    )
    
    if login_successful:
        logger.info("Login successful, trying to get apartments...")
        try:
            apartments = client.get_apartments()
            logger.info(f"Found {len(apartments)} apartments")
            
            # Print the first apartment if available
            if apartments:
                logger.info(f"First apartment: {json.dumps(apartments[0], indent=2)}")
        except Exception as e:
            logger.error(f"Error getting apartments: {e}")
    else:
        logger.error("Login failed, cannot proceed with API tests")

if __name__ == "__main__":
    test_api()