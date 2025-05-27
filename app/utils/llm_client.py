import httpx
from typing import Dict, Any, Optional
from ..config import MODEL_CONFIG, DEFAULT_MODEL

class LLMClient:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_config = MODEL_CONFIG.get(model_name)
        if not self.model_config:
            raise ValueError(f"Model {model_name} not found in configuration")
        
        self.base_url = self.model_config["base_url"]
        self.model_name = self.model_config["model_name"]
        self.timeout = self.model_config["timeout"]
        self.max_tokens = self.model_config["max_tokens"]
        self.temperature = self.model_config["temperature"]
        
        # 设置更详细的超时配置
        timeout = httpx.Timeout(
            connect=5.0,  # 连接超时
            read=self.timeout,  # 读取超时
            write=10.0,  # 写入超时
            pool=10.0  # 连接池超时
        )
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        调用大模型生成回复
        
        Args:
            prompt: 输入的提示词
            **kwargs: 其他参数，会覆盖默认配置
            
        Returns:
            Dict[str, Any]: 模型返回的结果
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
            }
            
            response = await self.client.post("/v1/chat/completions", json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            raise Exception(f"Error calling LLM API: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def close(self):
        """关闭HTTP客户端连接"""
        await self.client.aclose()

# 创建单例实例
llm_client = LLMClient() 