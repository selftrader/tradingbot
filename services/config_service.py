from typing import Dict
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConfigService:
    def __init__(self):
        self.config_path = "configs/trading_config.json"
        self._ensure_config_directory()

    def _ensure_config_directory(self):
        """Ensure config directory exists"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    async def save_config(self, config_data: Dict) -> Dict:
        """Save trading configuration"""
        try:
            config_data['updated_at'] = datetime.now().isoformat()
            
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            logger.info(f"Configuration saved successfully: {config_data}")
            return {"status": "success", "message": "Configuration saved successfully"}
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise