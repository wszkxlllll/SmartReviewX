# 产品评价生成系统 API 文档

## 概述

本文档详细说明了产品评价生成系统的所有API接口。系统提供评价生成、增强、质量检查等功能，基于大语言模型生成真实、自然、个性化的商品评价。

## 基础信息

- 基础URL: `http://localhost:8000`
- 所有请求和响应均使用JSON格式
- API文档地址：`http://localhost:8000/docs`
- Swagger UI地址：`http://localhost:8000/redoc`

## 数据模型

### UserBackground（用户背景）
```json
{
    "gender": "男",
    "age": 28,
    "occupation": "软件工程师",
    "income_level": "高",
    "experience": "精通",
    "tech_familiarity": "精通",
    "purchase_purpose": "工作需要",
    "region": "北京",
    "education_level": "硕士",
    "usage_frequency": "每天",
    "brand_loyalty": "高"
}
```

### ProductInfo（产品信息）
```json
{
    "name": "MacBook Pro M3",
    "category": "electronics",
    "brand": "Apple",
    "model_number": "M3 Pro",
    "specifications": {
        "CPU": "M3 Pro",
        "内存": "16GB",
        "存储": "512GB SSD",
        "屏幕": "14英寸 Liquid Retina XDR"
    },
    "warranty_period": "1年",
    "price_range": "高"
}
```

### GeneratedReview（生成的评价）
```json
{
    "content": "评价内容...",
    "rating": 4.5,
    "sentiment": "positive",
    "experience": "使用体验...",
    "pros": ["优点1", "优点2"],
    "cons": ["缺点1"],
    "sentiment_score": 0.9,
    "quality_score": 0.85,
    "user_background": {
        // 用户背景信息
    },
    "product_info": {
        // 产品信息
    }
}
```

## API 接口

### 1. 生成评价

```http
POST /generate_reviews
```

生成产品评价。

**请求体：**
```json
{
    "user_background": {
        // UserBackground对象
    },
    "product_info": {
        // ProductInfo对象
    },
    "num_reviews": 1  // 1-10之间的整数
}
```

**响应：**
```json
{
    "reviews": [
        // GeneratedReview对象数组
    ],
    "generation_time": 2.5  // 生成耗时（秒）
}
```

### 2. 增强评价

```http
POST /enhance_reviews
```

使用网络搜索功能增强评价内容。

**请求体：** 与生成评价接口相同

**响应：** 与生成评价接口相同，但评价内容更加丰富和专业

### 3. 检查评价质量

```http
POST /check_quality
```

检查单条评价的质量。

**请求体：**
```json
{
    "reviews": [
        // GeneratedReview对象
    ],
    "generation_time": 2.5
}
```

**响应：**
```json
{
    "status": "completed",
    "result": {
        "scores": {
            "真实性": 4.5,
            "一致性": 4.2,
            "具体性": 4.8,
            "语言自然度": 4.6
        },
        "overall_score": 4.5,
        "analysis": [
            "评价真实可信，符合用户背景特征",
            "内容连贯，逻辑清晰",
            "包含具体的使用体验和细节",
            "语言表达自然流畅"
        ]
    }
}
```

### 4. 批量检查评价质量

```http
POST /check_quality_batch
```

异步批量检查多条评价的质量。

**请求体：**
```json
{
    "reviews": [
        // GeneratedReview对象数组
    ],
    "generation_time": 2.5
}
```

**响应：**
```json
{
    "status": "processing",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "质量检查任务已启动"
}
```

### 5. 获取支持的产品类别

```http
GET /categories
```

获取系统支持的所有产品类别。

**响应：**
```json
{
    "categories": [
        "electronics",        // 电子产品
        "daily_necessities",  // 日用品
        "food_beverage",     // 食品饮料
        "clothing",          // 服装鞋帽
        "home_appliance",    // 家用电器
        "stationery"         // 教育文具
    ]
}
```

### 6. 获取评价统计信息

```http
GET /review_stats/{category}
```

获取指定类别的评价统计信息。

**响应：**
```json
{
    "total_reviews": 100,
    "average_rating": 4.5,
    "rating_distribution": {
        "1": 5,
        "2": 10,
        "3": 20,
        "4": 35,
        "5": 30
    },
    "sentiment_distribution": {
        "positive": 70,
        "neutral": 20,
        "negative": 10
    }
}
```

### 7. 健康检查

```http
GET /health
```

检查API服务是否正常运行。

**响应：**
```json
{
    "status": "healthy"
}
```

## 错误处理

所有接口在发生错误时会返回相应的HTTP状态码和错误信息：

```json
{
    "detail": "错误信息描述"
}
```

常见错误码：
- 400: 请求参数错误
- 404: 资源不存在
- 500: 服务器内部错误

## 使用示例

### Python示例

```python
import requests
import json

# 生成评价
def generate_reviews(user_background, product_info, num_reviews=1):
    response = requests.post(
        "http://localhost:8000/generate_reviews",
        json={
            "user_background": user_background,
            "product_info": product_info,
            "num_reviews": num_reviews
        }
    )
    return response.json()

# 检查评价质量
def check_quality(reviews):
    response = requests.post(
        "http://localhost:8000/check_quality",
        json={
            "reviews": reviews,
            "generation_time": 0
        }
    )
    return response.json()

# 批量检查评价质量
def check_quality_batch(reviews):
    response = requests.post(
        "http://localhost:8000/check_quality_batch",
        json={
            "reviews": reviews,
            "generation_time": 0
        }
    )
    return response.json()

# 使用示例
user_background = {
    "gender": "男",
    "age": 28,
    "occupation": "软件工程师",
    # ... 其他用户背景信息
}

product_info = {
    "name": "MacBook Pro M3",
    "category": "electronics",
    # ... 其他产品信息
}

# 生成评价
reviews = generate_reviews(user_background, product_info)

# 检查单条评价质量
quality_result = check_quality(reviews["reviews"])
print(json.dumps(quality_result, indent=2, ensure_ascii=False))

# 批量检查评价质量
batch_result = check_quality_batch(reviews["reviews"])
print(json.dumps(batch_result, indent=2, ensure_ascii=False))
```

## 注意事项

1. 评价生成数量限制在1-10条之间
2. 所有评价都会自动保存到data文件夹的CSV文件中
3. 评价统计信息会实时更新
4. 建议在生成评价后立即进行质量检查
5. 批量质量检查结果会保存在服务器的storage目录下 