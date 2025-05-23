# 智能商品评价生成系统

## 项目概述
本项目是一个基于大语言模型(LLM)的智能商品评价生成系统，能够根据用户背景和产品信息自动生成真实、自然、个性化的商品评价。系统采用模块化设计，支持多种商品类别的评价生成，并包含完整的质量控制机制。

## 系统架构

### 目录结构
```
backend/
├── models/                 # 数据模型和提示词模板
│   ├── data_model.py      # 数据模型定义
│   ├── category_prompts.py # 类别提示词模板
│   └── check_prompt.py    # 检查提示词模板
├── service/               # 核心服务
│   ├── routes.py         # API路由
│   ├── category_generators.py # 类别生成器
│   └── review_enhancer.py # 评价增强器
├── utils/                 # 工具函数
│   ├── quality_check.py  # 质量检查工具
│   └── review_saver.py   # 评价保存工具
├── docs/                  # 项目文档
│   └── api.md            # API文档
└── config.py             # 配置文件
```

## 核心功能

### 1. 智能评价生成
- 基于用户背景和产品信息的个性化评价生成
- 支持多种商品类别的专业评价生成
- 包含评分、评价内容、情感倾向等完整评价信息
- 支持批量生成评价
- 多级降级策略确保生成可靠性
- 生成的评价自动保存在data文件夹下

### 2. 类别提示词系统
- 支持多种商品类别的专业提示词模板
- 包含电子产品、日用品、食品饮料、服装鞋帽、家用电器、教育文具等类别
- 每个类别都有特定的评价维度和专业术语
- 动态提示词生成机制

### 3. 评价增强系统
- 基于网络搜索的信息补充
- 市场定位和竞品对比分析
- 最新用户反馈和评价趋势
- 技术参数和性能数据补充
- 使用场景和适用人群分析
- 异步批量处理能力

### 4. 质量控制机制
- 多维度质量评分系统
  - 真实性评分（1-5分）
    - 评价内容与用户背景的匹配度
    - 语气自然度
    - 用户特征体现程度
    - 使用习惯反映程度
  - 一致性评分（1-5分）
    - 评价观点一致性
    - 逻辑连贯性
    - 语气统一性
    - 结论合理性
  - 具体性评分（1-5分）
    - 使用场景具体程度
    - 产品特点描述详细度
    - 体验细节丰富度
    - 优缺点分析完整度
  - 语言自然度评分（1-5分）
    - 语言表达流畅度
    - 用词准确性
    - 语气真实度
    - 用户特征体现度
- 评价内容分析
  - 基于实际评分的多维度分析
  - 针对性改进建议
  - 质量趋势分析
- 批量质量检查
  - 异步并行处理
  - 批量结果统计
  - 质量分布分析
  - 批量质量检查的JSON返回值自动保存在storage文件夹下
- 评分标准
  - 5分：完全符合标准，表现优秀
  - 4分：基本符合标准，表现良好
  - 3分：部分符合标准，表现一般
  - 2分：较少符合标准，表现较差
  - 1分：完全不符合标准，表现差

## 技术特点

### 1. 模块化设计
- 基于工厂模式的服务生成
- 可扩展的类别支持系统
- 插件式的评价增强机制
- 灵活的质量控制体系

### 2. 高可用性设计
- 多级降级策略
- 异步任务处理
- 重试机制
- 错误处理
- 日志记录

### 3. 性能优化
- 异步并发处理
- 批量操作支持
- 缓存机制
- 资源池化

### 4. 安全性
- 输入验证
- 错误处理
- 日志记录
- 异常捕获

## API接口

### 1. 评价生成
```http
POST /generate_reviews
Content-Type: application/json
示例请求体：
{
  "user_background": {
    "gender": "男",
    "age": 35,
    "occupation": "软件架构师",
    "income_level": "较高",
    "experience": "非常熟练",
    "purchase_purpose": "家庭与工作两用",
    "usage_frequency": "每天",
    "region": "深圳"
  },
  "product_info": {
    "name": "小米14 Pro",
    "category": "electronics",
    "price_range": "4500-6000元",
    "features": ["徕卡影像", "第三代骁龙8", "LTPO OLED 屏幕", "120W快充", "IP68防水"]
  },
  "num_reviews": 1
}
```

### 2. 评价增强
```http
POST /enhance_reviews
Content-Type: application/json

{
    "reviews": [...]
}
```

### 3. 质量检查
```http
POST /check_quality
Content-Type: application/json
示例请求体：
{
  "reviews": [
    {
      "id": null,
      "user_background": {
        "gender": "男",
        "age": 35,
        "occupation": "软件架构师",
        "income_level": "较高",
        "experience": "非常熟练",
        "tech_familiarity": null,
        "purchase_purpose": "家庭与工作两用",
        "region": "深圳",
        "education_level": null,
        "usage_frequency": "每天",
        "brand_loyalty": null
      },
      "product_info": {
        "name": "小米14 Pro",
        "category": "electronics",
        "price_range": "4500-6000元",
        "features": [
          "徕卡影像",
          "第三代骁龙8",
          "LTPO OLED 屏幕",
          "120W快充",
          "IP68防水"
        ],
        "brand": null,
        "model_number": null,
        "specifications": null,
        "warranty_period": null,
        "expiration_date": null,
        "material": null,
        "weight": null,
        "dimensions": null,
        "package_info": null,
        "energy_efficiency": null,
        "safety_certifications": null,
        "usage_instructions": null,
        "additional_info": null
      },
      "rating": 5,
      "content": "作为一名软件架构师，我对小米14 Pro的性能和功能非常满意。第三代骁龙8处理器确保了无论是日常使用还是高强度工作都能流畅运行，LTPO OLED屏幕的显示效果令人印象深刻，色彩鲜艳且细节丰富。徕卡影像系统让拍照成为一种享受，照片质量远超预期。120W快充技术大大缩短了充电时间，非常适合忙碌的工作日。IP68防水等级让我在雨天使用时更加安心。系统流畅度和App兼容性都非常好，没有遇到任何问题。电池续航表现出色，即使是在高强度使用下也能轻松撑过一天。散热表现良好，长时间使用也不会感到过热。售后服务响应迅速，质保政策让人放心。总的来说，小米14 Pro是一款非常适合家庭与工作两用的高端智能手机，强烈推荐给追求性能和品质的用户。",
      "sentiment": "积极",
      "experience": "",
      "pros": [],
      "cons": [],
      "sentiment_score": 0.95,
      "quality_score": 0.95,
      "timeliness_analysis": null
    }
  ],
  "generation_time": 17.168129920959473
}

Response:
{
    "status": "completed",
    "result": {
        "scores": {
            "真实性": 4.5,
            "一致性": 4.0,
            "具体性": 4.5,
            "语言自然度": 4.0
        },
        "overall_score": 4.25,
        "analysis": [
            "评价真实可信，充分体现了用户的教育背景和职业特点",
            "内容连贯，逻辑清晰，观点前后一致",
            "包含具体的使用场景和体验细节，描述生动",
            "语言表达自然流畅，符合用户特征"
        ]
    }
}
```

## 使用示例

### 1. 生成评价
```python
from backend.models.data_model import UserBackground, ProductInfo
from backend.service.category_generators import ReviewGeneratorFactory

# 创建用户背景
user_background = UserBackground(
    gender="男",
    age=30,
    occupation="工程师",
    # ... 其他用户信息
)

# 创建产品信息
product_info = ProductInfo(
    name="智能手机",
    category="electronics",
    # ... 其他产品信息
)

# 获取对应类别的生成器
generator = ReviewGeneratorFactory.create_generator(product_info.category)

# 生成评价
review = generator.generate_review(user_background, product_info)
```

### 2. 增强评价
```python
from backend.service.review_enhancer import ReviewEnhancer

# 创建评价增强器
enhancer = ReviewEnhancer()

# 增强单个评价
enhanced_review = await enhancer.enhance_review(review)

# 批量增强评价
enhanced_reviews = await enhancer.enhance_reviews(reviews)
```

### 3. 质量检查
```python
from backend.utils.quality_check import QualityChecker

# 创建质量检查器
checker = QualityChecker()

# 检查单个评价
result = await checker.check_quality(review)

# 批量检查评价
results = checker.check_quality_batch(reviews)
```

## 开发计划

### 近期计划
- [ ] 优化提示词系统
- [ ] 增强质量控制机制
- [ ] 扩展商品类别支持
- [ ] 改进用户画像系统

### 中期计划
- [ ] 添加评价数据存储
- [ ] 实现评价统计分析
- [ ] 开发Web管理界面
- [ ] 优化性能表现

## 贡献指南
1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证
MIT License 
