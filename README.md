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
- 批量处理能力

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

## 使用教程

### 本地运行
拉取backend文件夹并执行pip install -r requirements.txt && python -m uvicorn backend.main:app --reload即可

### 1. 基本使用流程

#### 1.1 准备用户背景信息
```python
from backend.models.data_model import UserBackground

user_background = UserBackground(
    gender="男",
    age=30,
    occupation="工程师",
    income_level="中高收入",
    experience="专家",
    tech_familiarity="精通",
    purchase_purpose="自用",
    region="北京",
    education_level="硕士",
    usage_frequency="每天",
    brand_loyalty="高"
)
```

#### 1.2 准备产品信息
```python
from backend.models.data_model import ProductInfo

# 电子产品示例
electronics_info = ProductInfo(
    name="iPhone 15 Pro",
    category="electronics",
    price_range="高端",
    brand="Apple",
    model_number="A3096",
    specifications={
        "处理器": "A17 Pro",
        "内存": "8GB",
        "存储": "256GB",
        "屏幕": "6.1英寸 Super Retina XDR"
    },
    warranty_period="1年",
    features=["5G网络", "Pro相机系统", "钛金属边框"]
)

# 日用品示例
daily_necessities_info = ProductInfo(
    name="智能保温杯",
    category="daily_necessities",
    price_range="中端",
    brand="小米",
    material="304不锈钢",
    package_info="环保纸盒包装",
    features=["温度显示", "智能提醒", "保温12小时"]
)

# 食品饮料示例
food_beverage_info = ProductInfo(
    name="有机燕麦片",
    category="food_beverage",
    price_range="中端",
    brand="桂格",
    expiration_date="12个月",
    package_info="铝箔袋装",
    features=["有机认证", "无添加", "高纤维"]
)

# 服装鞋帽示例
clothing_info = ProductInfo(
    name="轻量羽绒服",
    category="clothing",
    price_range="中高端",
    brand="优衣库",
    material="90%白鸭绒",
    dimensions="M码",
    features=["轻便保暖", "可收纳", "防风防水"]
)

# 家用电器示例
home_appliance_info = ProductInfo(
    name="智能空气净化器",
    category="home_appliance",
    price_range="中高端",
    brand="小米",
    energy_efficiency="一级能效",
    warranty_period="2年",
    features=["HEPA过滤", "智能控制", "静音设计"]
)

# 教育文具示例
stationery_info = ProductInfo(
    name="智能笔记本",
    category="stationery",
    price_range="中端",
    brand="印象笔记",
    material="环保纸张",
    safety_certifications=["CE认证", "RoHS认证"],
    features=["云同步", "OCR识别", "多设备支持"]
)
```

#### 1.3 生成评价
```python
from backend.service.category_generators import ReviewGeneratorFactory

# 创建生成器
generator = ReviewGeneratorFactory.create_generator(product_info.category)

# 生成评价
review = generator.generate_review(user_background, product_info)
```

### 2. 类别特定功能

#### 2.1 电子产品 (electronics)
- 建议填写信息：型号、规格、保修期
- 特定评价维度：
  - 功能性能评估
  - 硬件配置分析
  - 软件体验评价
  - 电池续航表现
  - 散热性能
  - 售后服务评价

#### 2.2 日用品 (daily_necessities)
- 建议填写信息：材质、包装信息
- 特定评价维度：
  - 使用便捷性
  - 材质安全性
  - 耐用性评估
  - 价格合理性
  - 包装设计评价

#### 2.3 食品饮料 (food_beverage)
- 建议填写信息：有效期、包装信息
- 特定评价维度：
  - 口味评价
  - 包装安全性
  - 保质期评估
  - 营养价值分析
  - 价格合理性

#### 2.4 服装鞋帽 (clothing)
- 建议填写信息：材质、尺寸
- 特定评价维度：
  - 材质舒适度
  - 款式设计评价
  - 尺码合适性
  - 透气性评估
  - 洗护便捷性

#### 2.5 家用电器 (home_appliance)
- 建议填写信息：能效等级、保修期
- 特定评价维度：
  - 功能实用性
  - 能耗表现
  - 使用便捷性
  - 维护成本
  - 售后服务评价

#### 2.6 教育文具 (stationery)
- 建议填写信息：材质、安全认证
- 特定评价维度：
  - 使用安全性
  - 环保性评估
  - 实用性分析
  - 设计创新性
  - 价格合理性

### 3. API使用示例

#### 3.1 生成评价
```http
POST /generate_reviews
Content-Type: application/json

{
    "user_background": {
        "gender": "男",
        "age": 30,
        "occupation": "工程师",
        "income_level": "中高收入",
        "experience": "专家",
        "tech_familiarity": "精通",
        "purchase_purpose": "自用",
        "region": "北京",
        "education_level": "硕士",
        "usage_frequency": "每天",
        "brand_loyalty": "高"
    },
    "product_info": {
        "name": "iPhone 15 Pro",
        "category": "electronics",
        "price_range": "高端",
        "brand": "Apple",
        "model_number": "A3096",
        "specifications": {
            "处理器": "A17 Pro",
            "内存": "8GB",
            "存储": "256GB",
            "屏幕": "6.1英寸 Super Retina XDR"
        },
        "warranty_period": "1年",
        "features": ["5G网络", "Pro相机系统", "钛金属边框"]
    },
    "num_reviews": 1
}
```

#### 3.2 增强评价
```http
POST /enhance_reviews
Content-Type: application/json

{
    "user_background": {
        // 同上
    },
    "product_info": {
        // 同上
    },
    "num_reviews": 1
}
```

#### 3.3 质量检查

##### 3.3.1 单个评价质量检查
```http
POST /check_quality
Content-Type: application/json

{
  "reviews": [
    {
      "id": null,
      "user_background": {
        "gender": "男",
        "age": 30,
        "occupation": "工程师",
        "income_level": "中高收入",
        "experience": "专家",
        "tech_familiarity": "精通",
        "purchase_purpose": "自用",
        "region": "北京",
        "education_level": "硕士",
        "usage_frequency": "每天",
        "brand_loyalty": "高"
      },
      "product_info": {
        "name": "iPhone 15 Pro",
        "category": "electronics",
        "price_range": "高端",
        "features": [
          "5G网络",
          "Pro相机系统",
          "钛金属边框"
        ],
        "brand": "Apple",
        "model_number": "A3096",
        "specifications": {
          "处理器": "A17 Pro",
          "内存": "8GB",
          "存储": "256GB",
          "屏幕": "6.1英寸 Super Retina XDR"
        },
        "warranty_period": "1年",
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
      "content": "作为一名工程师，我对iPhone 15 Pro的性能和设计感到非常满意。A17 Pro处理器的运行速度令人印象深刻，无论是日常使用还是运行专业应用都毫无压力。8GB的内存和256GB的存储空间完全满足我的需求，Super Retina XDR屏幕的显示效果也非常出色。钛金属边框不仅美观，还增加了手机的耐用性。5G网络的加入让我的网络体验更上一层楼，Pro相机系统的拍照效果也非常专业。电池续航表现良好，能够支持我一天的高强度使用。散热方面，即使在长时间使用高性能应用时，手机也只是微温，表现令人满意。Apple的售后服务一直很可靠，1年的保修期也让我购买时更加放心。总的来说，iPhone 15 Pro是一款非常适合技术精通用户的高端手机。",
      "sentiment": "积极",
      "experience": "",
      "pros": [
        "A17 Pro处理器运行速度快",
        "8GB内存和256GB存储空间充足",
        "Super Retina XDR屏幕显示效果出色",
        "钛金属边框美观耐用",
        "5G网络体验优秀",
        "Pro相机系统拍照效果专业",
        "电池续航表现良好",
        "散热表现令人满意",
        "售后服务可靠"
      ],
      "cons": [
        "价格较高"
      ],
      "sentiment_score": 0.95,
      "quality_score": 0.95,
      "timeliness_analysis": null
    }
  ],
  "generation_time": 30.63783073425293
}
```

##### 3.3.2 批量质量检查
```http
POST /check_quality_batch
Content-Type: application/json

{
    "reviews": [
        {
            "id": null,
            "user_background": {
                "gender": "男",
                "age": 30,
                "occupation": "工程师",
                "income_level": "中高收入",
                "experience": "专家",
                "tech_familiarity": "精通",
                "purchase_purpose": "自用",
                "region": "北京",
                "education_level": "硕士",
                "usage_frequency": "每天",
                "brand_loyalty": "高"
            },
            "product_info": {
                "name": "iPhone 15 Pro",
                "category": "electronics",
                "price_range": "高端",
                "features": [
                    "5G网络",
                    "Pro相机系统",
                    "钛金属边框"
                ],
                "brand": "Apple",
                "model_number": "A3096",
                "specifications": {
                    "处理器": "A17 Pro",
                    "内存": "8GB",
                    "存储": "256GB",
                    "屏幕": "6.1英寸 Super Retina XDR"
                },
                "warranty_period": "1年"
            },
            "rating": 5,
            "content": "作为一名工程师，我对iPhone 15 Pro的性能和设计感到非常满意。A17 Pro处理器的运行速度令人印象深刻，无论是日常使用还是运行专业应用都毫无压力。8GB的内存和256GB的存储空间完全满足我的需求，Super Retina XDR屏幕的显示效果也非常出色。钛金属边框不仅美观，还增加了手机的耐用性。5G网络的加入让我的网络体验更上一层楼，Pro相机系统的拍照效果也非常专业。电池续航表现良好，能够支持我一天的高强度使用。散热方面，即使在长时间使用高性能应用时，手机也只是微温，表现令人满意。Apple的售后服务一直很可靠，1年的保修期也让我购买时更加放心。总的来说，iPhone 15 Pro是一款非常适合技术精通用户的高端手机。",
            "sentiment": "积极",
            "pros": [
                "A17 Pro处理器运行速度快",
                "8GB内存和256GB存储空间充足",
                "Super Retina XDR屏幕显示效果出色",
                "钛金属边框美观耐用",
                "5G网络体验优秀",
                "Pro相机系统拍照效果专业",
                "电池续航表现良好",
                "散热表现令人满意",
                "售后服务可靠"
            ],
            "cons": [
                "价格较高"
            ],
            "sentiment_score": 0.95,
            "quality_score": 0.95
        }
    ],
    "generation_time": 30.63783073425293
}
```

响应：
```json
{
    "status": "processing",
    "task_id": "53f7bde0-3122-4b6b-9b39-682c5087248d",
    "message": "质量检查任务已启动",
    "total_reviews": 1
}
```

##### 3.3.3 获取批量检查结果
```http
GET /check_quality_batch/53f7bde0-3122-4b6b-9b39-682c5087248d
```

如果任务正在处理中，返回：
```json
{
    "status": "processing",
    "task_id": "53f7bde0-3122-4b6b-9b39-682c5087248d",
    "message": "质量检查任务进行中",
    "total_reviews": 1,
    "processed_reviews": 0,
    "progress": "0/1"
}
```

如果任务已完成，返回：
```json
{
    "status": "completed",
    "task_id": "53f7bde0-3122-4b6b-9b39-682c5087248d",
    "message": "质量检查任务已完成",
    "total_reviews": 1,
    "results": [
        {
            "authenticity_score": 4.8,
            "consistency_score": 4.7,
            "specificity_score": 4.9,
            "language_score": 4.8,
            "overall_score": 4.8,
            "analysis": [
                "评价内容与用户背景高度匹配，体现了工程师的专业视角",
                "评价逻辑连贯，观点前后一致",
                "包含大量具体的技术参数和使用体验细节",
                "语言表达专业且自然，符合用户特征"
            ],
            "suggestions": [
                "可以补充更多与其他机型的对比信息",
                "建议添加一些具体的性能测试数据"
            ]
        }
    ],
    "start_time": "2024-03-14T10:00:00",
    "end_time": "2024-03-14T10:00:05"
}
```

如果任务失败，返回：
```json
{
    "status": "failed",
    "task_id": "53f7bde0-3122-4b6b-9b39-682c5087248d",
    "message": "质量检查任务失败",
    "error": "具体错误信息"
}
```

##### 3.3.4 批量质量检查使用说明
1. 首先调用 POST `/check_quality_batch` 接口提交评价列表，获取任务ID
2. 使用返回的任务ID调用 GET `/check_quality_batch/{task_id}` 接口查询结果
3. 如果任务还在处理中，可以定期轮询获取最新进度
4. 任务完成后，可以获取完整的质量检查结果
5. 如果任务失败，可以查看具体的错误信息

注意事项：
- 批量检查支持最多10条评价
- 建议在提交大量评价时使用批量检查接口
- 任务结果会保存在系统中，可以随时查询
- 建议定期清理已完成的任务结果

### 4. 错误处理
- 所有API调用都会返回标准的HTTP状态码
- 错误响应包含详细的错误信息
- 支持多级降级策略确保服务可用性
- 完整的日志记录系统

### 5. 最佳实践
1. 提供完整的用户背景信息以获得更个性化的评价
2. 确保产品信息符合类别要求
3. 使用批量生成时注意控制数量（1-10条）
4. 定期进行质量检查确保评价质量
5. 使用评价增强功能补充最新信息

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
