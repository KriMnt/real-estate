# test_imobiliare_api_noauth.py
import logging
import json
from app.services.api_clients.imobiliare_client import ImobiliareApiClient

# Set up detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_public_api():
    """Test ImobiliareRO API without authentication"""
    client = ImobiliareApiClient()
    
    # Test version endpoint first - this often works without auth
    logger.info("\n===== Testing get_version =====")
    version = client.get_version()
    logger.info(f"API Version: {version}")
    
    # Test apartments endpoint
    logger.info("\n===== Testing get_apartments without auth =====")
    apartments = client.get_apartments()
    logger.info(f"Found {len(apartments)} apartments")
    
    # Print sample apartment if available
    if apartments:
        logger.info(f"Sample apartment: {json.dumps(apartments[0], indent=2, ensure_ascii=False)}")
    
    # Test offers endpoint
    logger.info("\n===== Testing get_offers without auth =====")
    offers = client.get_offers()
    logger.info(f"Found {len(offers)} offers")
    
    # Print sample offer if available
    if offers:
        logger.info(f"Sample offer: {json.dumps(offers[0], indent=2, ensure_ascii=False)}")
    
    # Test all offers
    logger.info("\n===== Testing get_all_offers without auth =====")
    all_offers = client.get_all_offers()
    logger.info(f"Found {len(all_offers)} total offers")
    
    # Print sample from all offers if available
    if all_offers:
        logger.info(f"Sample from all offers: {json.dumps(all_offers[0], indent=2, ensure_ascii=False)}")
    
    # Summarize findings
    logger.info("\n===== API Testing Summary =====")
    logger.info(f"Version endpoint: {'Worked' if version else 'Failed'}")
    logger.info(f"Apartments endpoint: {'Worked' if apartments else 'Failed'}")
    logger.info(f"Offers endpoint: {'Worked' if offers else 'Failed'}")
    logger.info(f"All offers endpoint: {'Worked' if all_offers else 'Failed'}")

if __name__ == "__main__":
    test_public_api()