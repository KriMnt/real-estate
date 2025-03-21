# test_imobiliare_api.py
import logging
import sys
from app.services.api_clients.imobiliare_client import ImobiliareApiClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api():
    """Test the ImobiliareRO API client"""
    client = ImobiliareApiClient()
    
    # First, try to login
    logger.info("Testing login...")
    login_successful = client.login(
        username="your_username",  # Replace with actual credentials
        password="your_password"   # Replace with actual credentials
    )
    
    if not login_successful:
        logger.error("Login failed, cannot proceed with API tests")
        return
    
    # If login successful, try to get apartments
    logger.info("Testing get_apartments...")
    apartments = client.get_apartments()
    logger.info(f"Found {len(apartments)} apartments")
    
    # Print the first apartment if available
    if apartments:
        logger.info(f"First apartment: {apartments[0]}")
    
    # Try to get houses
    logger.info("Testing get_houses...")
    houses = client.get_houses()
    logger.info(f"Found {len(houses)} houses")
    
    # Print the first house if available
    if houses:
        logger.info(f"First house: {houses[0]}")

if __name__ == "__main__":
    test_api()