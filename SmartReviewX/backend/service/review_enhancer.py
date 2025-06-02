from openai import OpenAI
from typing import List, Dict, Optional, Any
from ..models.data_model import GeneratedReview
from ..config import settings
import json
import logging
import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class ReviewEnhancer:
    """评价增强处理类"""
    
    def __init__(self):
        """初始化评价增强器"""
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY2,
            base_url=settings.OPENAI_API_BASE2,
            timeout=30.0
        )
        self.search_api_url = settings.OPENAI_API_BASE2
        self.search_model = settings.OPENAI_API_MODEL2

    def _create_enhancement_prompt(self, review: GeneratedReview) -> str:
        """
        创建增强提示词
        
        Args:
            review: 原始评价对象
            
        Returns:
            增强提示词
        """
        return f"""请基于以下产品评价，使用网络搜索功能补充更多相关信息，使评价更加专业和可信：

产品名称：{review.product_info.name}
产品类别：{review.product_info.category}
产品品牌：{review.product_info.brand}
产品规格：{review.product_info.specifications}

原始评价：
{review.content}
{review.pros}
{review.cons}
请补充以下方面的信息：
1. 产品的市场定位和竞品对比
2. 最新的用户反馈和评价趋势
3. 相关的技术参数和性能数据
4. 产品的使用场景和适用人群

请保持评价的原有风格和情感倾向，只补充客观事实和数据。

请以JSON格式返回，包含以下字段：
- enhanced_content: 增强后的评价内容
- added_info: 补充的信息列表
- added_info_source: 补充信息的来源
- confidence_score: 补充信息的可信度(0-1)
"""

    def _search_with_ai(self, query: str) -> Dict:
        """使用AI搜索API获取信息"""
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的评价增强助手，擅长使用网络搜索获取产品相关信息。"},
                {"role": "user", "content": query}
            ]

            finish_reason = None
            while finish_reason is None or finish_reason == "tool_calls":
                response = self.client.chat.completions.create(
                    model="moonshot-v1-auto",  # 使用自动选择模型大小的版本
                    messages=messages,
                    temperature=0.3,
                    tools=[{
                        "type": "builtin_function",
                        "function": {
                            "name": "$web_search",
                        }
                    }]
                )
                
                choice = response.choices[0]
                finish_reason = choice.finish_reason
                
                if finish_reason == "tool_calls":
                    messages.append(choice.message)
                    for tool_call in choice.message.tool_calls:
                        if tool_call.function.name == "$web_search":
                            tool_call_arguments = json.loads(tool_call.function.arguments)
                            # 记录搜索消耗的tokens
                            search_tokens = tool_call_arguments.get("usage", {}).get("total_tokens", 0)
                            logger.info(f"搜索消耗tokens: {search_tokens}")
                            
                            # 返回搜索参数
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_call.function.name,
                                "content": json.dumps(tool_call_arguments)
                            })
                else:
                    # 当finish_reason为stop时，返回最终的内容
                    return choice.message.content

        except Exception as e:
            logger.error(f"搜索API调用失败: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"API响应状态码: {e.response.status_code}")
                logger.error(f"API错误信息: {e.response.text}")
            raise

    def _call_enhancement_api(self, prompt: str) -> Dict:
        """调用API进行评价增强"""
        try:
            # 首先进行网络搜索
            search_result = self._search_with_ai(prompt)
            
            # 使用搜索结果增强评价
            response = self.client.chat.completions.create(
                model="moonshot-v1-auto",
                messages=[
                    {"role": "system", "content": "你是一个专业的评价增强助手。请基于搜索结果，将补充的信息自然地融入到原始评价中，以联网信息为准，保持评价的连贯性和可读性。"},
                    {"role": "user", "content": f"""原始评价：
{prompt}

搜索结果：
{search_result}

请将搜索结果中的信息自然地融入到原始评价中，生成一个完整的、连贯的评价。保持原有的评价风格和情感倾向，只补充客观事实和数据。

请以JSON格式返回，必须包含以下字段：
- enhanced_content: 增强后的评价内容
- added_info: 补充的信息列表
- confidence_score: 补充信息的可信度(0-1)
- pros: 产品的优点列表
- cons: 产品的缺点列表"""}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("API响应内容为空")
                
            try:
                result = json.loads(content)
                required_fields = ["enhanced_content", "added_info", "confidence_score", "pros", "cons"]
                if not all(field in result for field in required_fields):
                    missing_fields = [field for field in required_fields if field not in result]
                    raise ValueError(f"响应缺少必要字段: {', '.join(missing_fields)}")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析错误: {str(e)}")
                logger.error(f"原始响应内容: {content}")
                raise
                
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"API响应状态码: {e.response.status_code}")
                logger.error(f"API错误信息: {e.response.text}")
            raise

    def enhance_review(self, review: GeneratedReview) -> GeneratedReview:
        """
        增强评价内容
        
        Args:
            review: 原始评价对象
            
        Returns:
            增强后的评价对象
        """
        try:
            # 创建增强提示词
            prompt = self._create_enhancement_prompt(review)
            
            # 调用API进行增强
            result = self._call_enhancement_api(prompt)
            
            # 更新评价对象
            review.content = result["enhanced_content"]
            review.pros = result.get("pros", review.pros)  # 如果API没有返回pros，保留原有的
            review.cons = result.get("cons", review.cons)  # 如果API没有返回cons，保留原有的
            review.quality_score = min(1.0, review.quality_score + 0.1)
            
            # 记录补充的信息
            logger.info(f"评价增强成功，补充信息: {result['added_info']}")
            logger.info(f"补充信息可信度: {result['confidence_score']}")
            
            return review
            
        except Exception as e:
            logger.error(f"评价增强失败: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"API响应状态码: {e.response.status_code}")
                logger.error(f"API错误信息: {e.response.text}")
            # 发生错误时保留原有评价内容
            return review
            
    def enhance_reviews(self, reviews: List[GeneratedReview]) -> List[GeneratedReview]:
        """
        批量增强评价内容
        
        Args:
            reviews: 原始评价列表
            
        Returns:
            增强后的评价列表
        """
        try:
            enhanced_reviews = []
            for review in reviews:
                enhanced_review = self.enhance_review(review)
                enhanced_reviews.append(enhanced_review)
            return enhanced_reviews
        except Exception as e:
            logger.error(f"批量增强评价失败: {str(e)}")
            return reviews 
