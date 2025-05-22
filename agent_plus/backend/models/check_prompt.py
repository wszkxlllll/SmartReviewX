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

请从1-5分评估这段评价的真实性，评分标准如下：
5分：评价内容与用户背景高度匹配，语气自然，重点突出，充分体现用户特征和使用习惯
4分：评价内容与用户背景基本匹配，语气较自然，基本体现用户特征
3分：评价内容与用户背景部分匹配，语气一般，部分体现用户特征
2分：评价内容与用户背景匹配度较低，语气生硬，较少体现用户特征
1分：评价内容与用户背景完全不匹配，语气不自然，未能体现用户特征

请以JSON格式返回，示例格式如下：
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

请从1-5分评估这段评价的一致性，评分标准如下：
5分：评价观点完全一致，逻辑严密，语气统一，结论合理
4分：评价观点基本一致，逻辑较连贯，语气较统一
3分：评价观点部分一致，逻辑一般，语气基本统一
2分：评价观点不够一致，逻辑不够连贯，语气不够统一
1分：评价观点前后矛盾，逻辑混乱，语气不一致

请以JSON格式返回，示例格式如下：
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

请从1-5分评估这段评价的具体性，评分标准如下：
5分：包含丰富的具体使用场景、产品特点、体验细节和优缺点
4分：包含较多具体使用场景、产品特点和体验细节
3分：包含部分具体使用场景和产品特点
2分：具体使用场景和产品特点较少
1分：完全没有具体使用场景和产品特点

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

请从1-5分评估这段评价的语言自然度，评分标准如下：
5分：语言表达非常自然流畅，用词准确，语气真实，充分体现用户特征
4分：语言表达较为自然流畅，用词较准确，语气较真实
3分：语言表达一般，用词基本准确，语气基本真实
2分：语言表达不够自然，用词不够准确，语气不够真实
1分：语言表达完全不自然，用词不准确，语气不真实

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
        return f"""请根据以下评分结果对用户评价进行质量分析：

评价内容：
{review}

质量评分：
{', '.join([f'{k}: {v:.1f}' for k, v in scores.items()])}

请根据实际评分结果，从以下维度进行分析：
1. 真实性（{scores['真实性']:.1f}分）：评价内容是否符合用户背景特征
2. 一致性（{scores['一致性']:.1f}分）：评价观点是否前后一致，逻辑是否连贯
3. 具体性（{scores['具体性']:.1f}分）：是否包含具体的使用场景和体验细节
4. 语言自然度（{scores['语言自然度']:.1f}分）：表达是否自然，是否符合用户特征

请以JSON格式返回分析结果，示例格式如下：
{{
    "analysis": [
        "评价真实可信，充分体现了用户的教育背景和职业特点",
        "内容连贯，逻辑清晰，观点前后一致",
        "包含具体的使用场景和体验细节，描述生动",
        "语言表达自然流畅，符合用户特征"
    ]
}}"""

