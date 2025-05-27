# 评审服务实现，后续补充 
from typing import Dict, List, Optional
from app.models.schemas import ReviewRequest, FileContent
from app.core.model_selector import ModelSelector
from app.utils.llm_client import LLMClient
import json
import uuid
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self):
        self.model_selector = ModelSelector()
    
    async def generate_review_report(self, request: ReviewRequest) -> Dict:
        """
        生成代码评审报告
        
        Args:
            request: ReviewRequest对象，包含评审请求的所有信息
            
        Returns:
            Dict: 评审报告，包含评审结果和建议
        """
        # 1. 根据请求类型选择模型
        model = self.model_selector.select_model(
            model_type=request.model_type,
            client_type=request.client_type,
            review_mode=request.review_mode
        )
        
        # 2. 根据评审模式处理代码
        code_content = self._process_code_content(request)
        
        # 3. 生成评审报告
        review_report = await self._generate_report(model, code_content, request)
        
        return review_report
    
    def _process_code_content(self, request: ReviewRequest) -> str:
        """
        根据不同的评审模式处理代码内容
        """
        if request.review_mode == 'file':
            return self._process_file_mode(request.files)
        elif request.review_mode == 'commit':
            return self._process_commit_mode(request.diff)
        elif request.review_mode == 'snippet':
            return self._process_snippet_mode(request.code_snippet)
        else:
            raise ValueError(f"不支持的评审模式: {request.review_mode}")
    
    def _process_file_mode(self, files: Optional[List[FileContent]]) -> str:
        """处理文件模式"""
        if not files:
            raise ValueError("文件列表为空")

        processed_content = []
        for file in files:
            # 如果 file 是 dict，转为 FileContent
            if isinstance(file, dict):
                file = FileContent(**file)
            file_header = f"=== 文件: {file.path} ==="
            if getattr(file, 'language', None):
                file_header += f" [语言: {file.language}]"
            processed_content.append(file_header)
            processed_content.append(str(file.content))
            processed_content.append("=" * 50)  # 分隔符
        return "\n".join(processed_content)
    
    def _process_commit_mode(self, diff: Optional[str]) -> str:
        """处理提交模式"""
        if not diff:
            raise ValueError("差异内容为空")
        return diff
    
    def _process_snippet_mode(self, code_snippet: Optional[str]) -> str:
        """处理代码片段模式"""
        if not code_snippet:
            raise ValueError("代码片段为空")
        return code_snippet
    
    async def _generate_report(self, model: str, code_content: str, request: ReviewRequest) -> Dict:
        """
        生成评审报告
        
        Args:
            model: 模型名称
            code_content: 代码内容
            request: 评审请求对象
            
        Returns:
            Dict: 评审报告
        """
        # 创建LLM客户端
        llm_client = LLMClient(model_name=model)
        
        try:
            # 构建提示词
            prompt = self._build_review_prompt(code_content, request)
            logger.info(f"Generated prompt: {prompt}")
            
            # 调用模型生成评审报告
            response = await llm_client.generate(prompt)
            logger.info(f"Model response: {response}")
            
            # 解析模型返回的结果
            review_result = self._parse_model_response(response)
            logger.info(f"Parsed review result: {review_result}")
            
            # 构建最终的评审报告
            report = {
                "review_id": f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
                "client_type": request.client_type,
                "review_mode": request.review_mode,
                "model_type": model,
                "summary": review_result.get("summary", {
                    "overall_score": 0,
                    "issues_found": 0,
                    "suggestions": 0
                }),
                "issues": review_result.get("issues", []),
                "suggestions": review_result.get("suggestions", []),
                "code_quality": review_result.get("code_quality", {
                    "complexity": "unknown",
                    "maintainability": "unknown",
                    "test_coverage": "unknown"
                })
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
        finally:
            # 确保关闭LLM客户端
            await llm_client.close()
    
    def _build_review_prompt(self, code_content: str, request: ReviewRequest) -> str:
        """
        构建评审提示词
        
        Args:
            code_content: 代码内容
            request: 评审请求对象
            
        Returns:
            str: 提示词
        """
        prompt = f"""请对以下代码进行评审分析，并以JSON格式返回中文评审报告。评审报告应包含以下字段：
1. summary: 包含overall_score(0-100的评分)、issues_found(发现的问题数量)、suggestions(改进建议数量)
2. issues: 问题列表，每个问题包含：
   - type: 问题类型（如：安全性、性能、可维护性等）
   - severity: 严重程度（高、中、低）
   - description: 问题描述（中文）
   - location: 问题位置（如：第X行）
   - suggestion: 改进建议（中文）
3. suggestions: 建议列表，每个建议包含：
   - type: 建议类型（如：性能优化、代码规范、最佳实践等）
   - description: 建议描述（中文）
   - location: 建议位置（如：第X行）
4. code_quality: 包含：
   - complexity: 代码复杂度（高、中、低）
   - maintainability: 可维护性（好、中、差）
   - test_coverage: 测试覆盖率（完整、部分、无）

评审模式: {request.review_mode}
客户端类型: {request.client_type}

代码内容:
{code_content}

请以JSON格式返回中文评审报告，确保返回的是合法的JSON格式。评审报告应该：
1. 使用中文描述所有问题和建议
2. 评分和建议要具体且有建设性
3. 问题描述要清晰明确
4. 建议要具有可操作性"""

        return prompt
    
    def _parse_model_response(self, response: Dict) -> Dict:
        """
        解析模型返回的结果
        """
        try:
            # 从模型响应中提取内容
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            logger.info(f"Extracted content from response: {content}")
            
            # 清理内容，移除可能的markdown标记
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # 解析JSON内容
            review_result = json.loads(content)
            logger.info(f"Successfully parsed review result: {review_result}")
            return review_result
            
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"Error parsing model response: {str(e)}")
            # 如果解析失败，返回默认结果
            return {
                "summary": {
                    "overall_score": 0,
                    "issues_found": 0,
                    "suggestions": 0
                },
                "issues": [],
                "suggestions": [],
                "code_quality": {
                    "complexity": "unknown",
                    "maintainability": "unknown",
                    "test_coverage": "unknown"
                }
            } 