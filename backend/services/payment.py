from typing import Optional, Dict, Any
import requests
from ..config import settings
from ..utils import generate_order_id

class PaymentService:
    def __init__(self):
        self.paykassa_settings = {
            "merchant_id": settings.PAYKASSA_MERCHANT_ID,
            "merchant_password": settings.PAYKASSA_MERCHANT_PASSWORD,
            "api_id": settings.PAYKASSA_API_ID,
            "api_password": settings.PAYKASSA_API_PASSWORD,
            "test": settings.PAYKASSA_TEST_MODE
        }
        
        self.freekassa_settings = {
            "merchant_id": settings.FREEKASSA_MERCHANT_ID,
            "secret_key": settings.FREEKASSA_SECRET_KEY,
            "api_key": settings.FREEKASSA_API_KEY,
            "test": settings.FREEKASSA_TEST_MODE
        }

    async def create_paykassa_payment(
        self,
        amount: float,
        currency: str = "USD",
        payment_system: str = "card",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание платежа через PayKassa"""
        order_id = generate_order_id()
        
        data = {
            "func": "api_payment",
            "merchant_id": self.paykassa_settings["merchant_id"],
            "merchant_password": self.paykassa_settings["merchant_password"],
            "api_id": self.paykassa_settings["api_id"],
            "api_password": self.paykassa_settings["api_password"],
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "system": payment_system,
            "test": self.paykassa_settings["test"]
        }
        
        if description:
            data["description"] = description
            
        response = requests.post(
            "https://paykassa.pro/api/0.5/index.php",
            json=data
        )
        
        result = response.json()
        if result.get("error"):
            raise Exception(f"PayKassa error: {result['error']}")
            
        return {
            "order_id": order_id,
            "payment_url": result["data"]["url"],
            "payment_id": result["data"]["transaction"]
        }

    async def create_freekassa_payment(
        self,
        amount: float,
        currency: str = "RUB",
        payment_system: str = "card",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание платежа через FreeKassa"""
        order_id = generate_order_id()
        
        data = {
            "m": self.freekassa_settings["merchant_id"],
            "oa": amount,
            "o": order_id,
            "s": self._generate_freekassa_signature(order_id, amount),
            "currency": currency,
            "lang": "ru"
        }
        
        if description:
            data["i"] = description
            
        if payment_system:
            data["pay"] = payment_system
            
        if self.freekassa_settings["test"]:
            data["test"] = 1
            
        return {
            "order_id": order_id,
            "payment_url": f"https://pay.freekassa.ru/?{self._build_query_string(data)}"
        }

    def _generate_freekassa_signature(self, order_id: str, amount: float) -> str:
        """Генерация подписи для FreeKassa"""
        import hashlib
        signature = f"{self.freekassa_settings['merchant_id']}:{amount}:{self.freekassa_settings['secret_key']}:{order_id}"
        return hashlib.md5(signature.encode()).hexdigest()

    def _build_query_string(self, data: Dict[str, Any]) -> str:
        """Построение строки запроса"""
        return "&".join(f"{k}={v}" for k, v in data.items())

    async def check_paykassa_payment(self, order_id: str) -> Dict[str, Any]:
        """Проверка статуса платежа PayKassa"""
        data = {
            "func": "api_payment_status",
            "merchant_id": self.paykassa_settings["merchant_id"],
            "merchant_password": self.paykassa_settings["merchant_password"],
            "api_id": self.paykassa_settings["api_id"],
            "api_password": self.paykassa_settings["api_password"],
            "order_id": order_id
        }
        
        response = requests.post(
            "https://paykassa.pro/api/0.5/index.php",
            json=data
        )
        
        result = response.json()
        if result.get("error"):
            raise Exception(f"PayKassa error: {result['error']}")
            
        return result["data"]

    async def check_freekassa_payment(self, order_id: str) -> Dict[str, Any]:
        """Проверка статуса платежа FreeKassa"""
        data = {
            "shopId": self.freekassa_settings["merchant_id"],
            "nonce": order_id,
            "signature": self._generate_freekassa_signature(order_id, 0)
        }
        
        response = requests.post(
            "https://api.freekassa.ru/v1/orders/status",
            json=data,
            headers={"Authorization": f"Bearer {self.freekassa_settings['api_key']}"}
        )
        
        result = response.json()
        if result.get("error"):
            raise Exception(f"FreeKassa error: {result['error']}")
            
 