from typing import Dict, Optional
from app.models.schemas import ReviewRequest

class ModelSelector:
    """模型选择器，根据客户端类型和评审模式选择合适的模型"""
    
    # 模型配置
    MODEL_14B = "qwen2.5-coder-14b-instruct"
    MODEL_32B = "qwen2.5-coder-32b-instruct"
    
    # 客户端类型
    CLIENT_VSCODE = "vscode"
    CLIENT_GERRIT = "gerrit"
    
    # 评审模式
    MODE_SNIPPET = "snippet"
    MODE_COMMIT = "commit"
    MODE_FILE = "file"
    
    def __init__(self):
        # 模型选择规则配置
        self.model_rules = {
            self.CLIENT_VSCODE: {
                self.MODE_SNIPPET: self.MODEL_14B,
                self.MODE_COMMIT: self.MODEL_14B,
                self.MODE_FILE: self.MODEL_32B
            },
            self.CLIENT_GERRIT: {
                # Gerrit端默认使用32b模型
                self.MODE_SNIPPET: self.MODEL_32B,
                self.MODE_COMMIT: self.MODEL_32B,
                self.MODE_FILE: self.MODEL_32B
            }
        }
    
    def select_model(self, model_type: str, client_type: str, review_mode: str) -> str:
        """
        根据请求选择合适的模型
        
        Args:
            model_type: 请求的模型类型
            client_type: 客户端类型
            review_mode: 评审模式
            
        Returns:
            str: 选择的模型名称
            
        Raises:
            ValueError: 当客户端类型或评审模式无效时
        """
        # 验证客户端类型
        if client_type not in [self.CLIENT_VSCODE, self.CLIENT_GERRIT]:
            raise ValueError(f"不支持的客户端类型: {client_type}")
            
        # 验证评审模式
        if review_mode not in [self.MODE_SNIPPET, self.MODE_COMMIT, self.MODE_FILE]:
            raise ValueError(f"不支持的评审模式: {review_mode}")
        
        # 获取模型选择规则
        client_rules = self.model_rules.get(client_type)
        if not client_rules:
            raise ValueError(f"未找到客户端类型 {client_type} 的模型规则")
            
        # 选择模型
        selected_model = client_rules.get(review_mode)
        if not selected_model:
            raise ValueError(f"未找到评审模式 {review_mode} 的模型规则")
            
        return selected_model
    
    def get_model_info(self, model_name: str) -> Dict:
        """
        获取模型信息
        
        Args:
            model_name: 模型名称
            
        Returns:
            Dict: 模型信息
        """
        model_info = {
            self.MODEL_14B: {
                "name": "14B模型",
                "description": "适用于代码片段和提交评审的轻量级模型",
                "max_tokens": 4096,
                "capabilities": ["代码分析", "安全检查", "性能优化建议"]
            },
            self.MODEL_32B: {
                "name": "32B模型",
                "description": "适用于文件级评审和复杂场景的高级模型",
                "max_tokens": 8192,
                "capabilities": ["深度代码分析", "架构评估", "完整安全审计", "性能优化"]
            }
        }
        
        return model_info.get(model_name, {}) 