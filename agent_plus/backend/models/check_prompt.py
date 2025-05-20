from typing import Dict, Any, List
from .data_model import UserBackground, ProductInfo


class CheckPromptTemplate:
   
    @staticmethod
    def check_authenticity_prompt(review: str, user_background: UserBackground) -> str:
        """检查评价真实性的提示词模板"""
        return f"""请评估以下用户评价的真实性：

评价内容：
{review}

用户背景：
- 性别：{user_background.gender}
- 年龄：{user_background.age}
- 职业：{user_background.occupation}
- 收入水平：{user_background.income_level}
- 使用经验：{user_background.experience}
- 技术熟悉度：{user_background.tech_familiarity}
- 购买目的：{user_background.purchase_purpose}
- 地区：{user_background.region}
- 教育程度：{user_background.education_level}
- 使用频率：{user_background.usage_frequency}
- 品牌忠诚度：{user_background.brand_loyalty}

请从1-5分评估这段评价的真实性，考虑：
1. 评价内容是否符合用户背景特征
2. 评价语气是否自然
3. 评价重点是否符合用户特征
4. 评价细节是否合理
5. 评价是否反映用户的使用频率和品牌忠诚度
6. 评价是否体现用户的教育水平和地区特点

请以JSON格式返回，示例格式如下：
eg1:
{{
    "score": 4.5,
    "reason": "评价内容与用户背景相符，语气自然，重点突出，体现了用户的使用习惯和品牌偏好"
}}
eg2:
{{
    "score": 3.5,
    "reason": "评价内容与用户背景基本相符，但缺乏对用户使用频率和品牌忠诚度的体现"
}}
eg3:
{{
    "score": 1.5,
    "reason": "评价内容与用户背景完全不符，语气生硬，未能体现用户特征和使用习惯"
}}"""

    @staticmethod
    def check_consistency_prompt(review: str) -> str:
        """检查评价一致性的提示词模板"""
        return f"""请评估以下用户评价的一致性：

评价内容：
{review}

请从1-5分评估这段评价的一致性，考虑：
1. 评价观点是否前后一致
2. 评价重点是否突出
3. 评价逻辑是否连贯
4. 评价结论是否合理
5. 评价内容是否与用户背景保持一致
6. 评价语气是否统一

请以JSON格式返回，示例格式如下：
eg1:
{{
    "score": 4.5,
    "reason": "评价观点前后一致，逻辑连贯，语气统一"
}}
eg2:
{{
    "score": 3.5,
    "reason": "评价观点基本一致，但部分内容逻辑不够连贯"
}}
eg3:
{{
    "score": 1.5,
    "reason": "评价观点前后矛盾，逻辑混乱，语气不一致"
}}
"""

    @staticmethod
    def check_specificity_prompt(review: str) -> str:
        """检查评价具体性的提示词模板"""
        return f"""请评估以下用户评价的具体性：

评价内容：
{review}

请从1-5分评估这段评价的具体性，考虑：
1. 是否包含具体的使用场景
2. 是否描述具体的产品特点
3. 是否提供具体的体验细节
4. 是否给出具体的优缺点
5. 是否包含具体的使用频率和场景
6. 是否提供具体的品牌对比和选择理由

请以JSON格式返回，示例格式如下：
eg1:
{{
    "score": 4.5,
    "reason": "评价包含具体的使用场景、产品特点和使用体验，并提供了详细的品牌对比"
}}
eg2:
{{
    "score": 3.5,
    "reason": "评价较为缺乏具体的使用场景和产品特点，但基本描述了使用体验"
}}
eg3:
{{
    "score": 1.5,
    "reason": "评价完全没有具体的使用场景和产品特点，内容过于笼统"
}}
"""

    @staticmethod
    def check_language_naturalness_prompt(review: str) -> str:
        """检查评价语言自然度的提示词模板"""
        return f"""请评估以下用户评价的语言自然度：

评价内容：
{review}

请从1-5分评估这段评价的语言自然度，考虑：
1. 语言表达是否自然流畅
2. 用词是否符合用户特征
3. 语气是否真实自然
4. 是否避免过于营销化的表达
5. 是否体现用户的教育水平和专业背景
6. 是否使用符合用户年龄和职业的表达方式

请以JSON格式返回，示例格式如下：
eg1:
{{
    "score": 4.5,
    "reason": "语言表达自然流畅，符合用户特征，体现了用户的教育背景和职业特点"
}}
eg2:
{{
    "score": 3.5,
    "reason": "语言表达较为生硬，部分用词不符合用户特征"
}}
eg3:
{{
    "score": 1.5,
    "reason": "语言表达完全不自然，用词和语气与用户特征不符"
}}
"""

    @staticmethod
    def generate_analysis_prompt(review: str, scores: Dict[str, float]) -> str:
        """生成质量分析报告的提示词模板"""
        return f"""请对以下用户评价进行质量分析：

评价内容：
{review}

质量评分：
{', '.join([f'{k}: {v:.1f}' for k, v in scores.items()])}

请从以下维度进行分析：
1. 真实性：评价内容是否符合用户背景特征
2. 一致性：评价观点是否前后一致，逻辑是否连贯
3. 具体性：是否包含具体的使用场景和体验细节
4. 语言自然度：表达是否自然，是否符合用户特征
5. 用户特征体现：是否充分体现用户的教育水平、使用频率和品牌偏好
6. 产品特点描述：是否准确描述产品特点和优势

请以JSON格式返回分析结果，示例格式如下：
eg1:
{{
    "analysis": [
        "评价真实可信，充分体现了用户的教育背景和职业特点",
        "内容连贯，逻辑清晰，观点前后一致",
        "包含具体的使用场景和体验细节，描述生动",
        "语言表达自然流畅，符合用户特征",
        "充分体现了用户的使用频率和品牌偏好",
        "准确描述了产品特点和优势"
    ]
}}"""

