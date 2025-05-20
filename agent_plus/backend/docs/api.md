# 产品评价生成系统 API 文档

## 概述

本文档详细说明了产品评价生成系统的所有API接口。系统提供评价生成、增强、质量检查等功能。

## 基础信息

- 基础URL: `http://localhost:8000`
- 所有请求和响应均使用JSON格式
- 认证方式：API密钥（在请求头中设置 `X-API-Key`）

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
    },
    "product_info": {
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
    },
    "num_reviews": 1
}
```

**响应：**
```json
{
    "reviews": [
        {
            "content": "评价内容...",
            "rating": 4.5,
            "sentiment": "positive",
            "experience": "使用体验...",
            "pros": ["优点1", "优点2"],
            "cons": ["缺点1"],
            "sentiment_score": 0.9,
            "quality_score": 0.85
        }
    ],
    "generation_time": 2.5
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

异步检查单条评价的质量。

**请求体：**
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

**响应：**
```json
{
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "message": "质量检查任务已提交，请使用task_id查询结果"
}
```

### 3.1 获取质量检查结果

```http
GET /quality_check_result/{task_id}
```

获取质量检查任务的结果。

**参数：**
- **task_id**: 任务ID（从检查评价质量接口获取）

**响应：**
```json
{
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
```

如果任务仍在处理中：
```json
{
    "status": "processing",
    "message": "质量检查任务正在处理中"
}
```

### 4. 批量检查评价质量

```http
POST /check_quality_batch
```

异步批量检查多条评价的质量。

**请求体：**
```json
[
    {
        // 评价1
    },
    {
        // 评价2
    }
]
```

**响应：**
```json
{
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "message": "批量质量检查任务已提交，请使用task_id查询结果"
}
```

使用相同的 `/quality_check_result/{task_id}` 接口获取批量检查结果。

### 5. 获取支持的产品类别

```http
GET /categories
```

获取系统支持的所有产品类别。

**响应：**
```json
{
    "categories": [
        "electronics",
        "daily_necessities",
        "food_beverage",
        "clothing",
        "home_appliance",
        "stationery"
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
    "avg_rating": 4.5,
    "avg_sentiment_score": 0.85,
    "avg_quality_score": 0.88
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
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误

## 使用示例

### Python示例

```python
import requests
import time

# 设置API密钥
headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

# 生成评价
response = requests.post(
    "http://localhost:8000/generate_reviews",
    headers=headers,
    json={
        "user_background": {...},
        "product_info": {...},
        "num_reviews": 1
    }
)

# 提交质量检查任务
quality_task = requests.post(
    "http://localhost:8000/check_quality",
    headers=headers,
    json=response.json()["reviews"][0]
)
task_id = quality_task.json()["task_id"]

# 轮询检查结果
while True:
    result = requests.get(
        f"http://localhost:8000/quality_check_result/{task_id}",
        headers=headers
    )
    if result.json().get("status") != "processing":
        break
    time.sleep(1)  # 等待1秒后再次检查

# 获取最终结果
final_result = result.json()
print(final_result)
```

### cURL示例

```bash
# 生成评价
curl -X POST "http://localhost:8000/generate_reviews" \
     -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"user_background": {...}, "product_info": {...}, "num_reviews": 1}'

# 提交质量检查任务
curl -X POST "http://localhost:8000/check_quality" \
     -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"content": "...", ...}'

# 获取检查结果
curl -X GET "http://localhost:8000/quality_check_result/{task_id}" \
     -H "X-API-Key: your-api-key"
```

## 注意事项

1. 所有请求都需要包含有效的API密钥
2. 评价生成数量限制在1-10条之间
3. 质量检查采用异步方式，需要轮询获取结果
4. 建议使用1-2秒的轮询间隔
5. 任务结果会在获取后自动删除
6. 增强评价功能需要额外的API调用，可能会产生额外费用
7. 建议在生成评价后立即进行质量检查 