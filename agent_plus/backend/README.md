# 基于大语言模型的产品评价生成系统

这是一个基于大语言模型（LLM）的产品评价生成系统，使用 FastAPI 构建后端服务。系统能够根据用户背景和产品信息，生成真实、自然、个性化的用户评价。

## 核心技术

1. 大语言模型（LLM）：
   - 使用 chatecnu 提供的大模型和 OpenAI GPT 和 deepseek 作为核心生成引擎
   - 支持联网搜索增强评价内容
   - 实现 Chain of Thought 推理
   - 支持 Self-Consistency 一致性检查
   - 提供情感和质量置信度评分

2. 智能评价生成：
   - 基于用户背景生成个性化评价
   - 考虑产品特点和用户需求
   - 确保评价的真实性和相关性
   - 支持批量生成评价

3. 评价质量控制：
   - 情感倾向分析
   - 质量评分机制
   - 自动重试机制
   - 评价一致性检查
   - 异步质量检查任务

4. 评价增强功能：
   - 使用 OpenAI 的联网搜索功能
   - 补充市场定位和竞品对比
   - 添加最新用户反馈和评价趋势
   - 补充技术参数和性能数据
   - 增强使用场景和适用人群分析

5. 数据管理：
   - 自动保存生成的评价到 CSV 文件
   - 按类别和日期组织评价数据
   - 提供评价统计信息

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量：
# OPENAI_API_KEY=your-api-key
# OPENAI_API_BASE=your-api-base
# OPENAI_API_MODEL=your-model-name
# SECRET_KEY=your-secret-key
```

3. 运行服务：
```bash
uvicorn main:app --reload
```

## 大模型配置

1. 基础配置：
   - OPENAI_API_KEY：OpenAI API 密钥
   - OPENAI_API_BASE：API 基础 URL
   - OPENAI_API_MODEL：使用的模型名称

2. 模型参数：
   - LLM_TEMPERATURE：生成温度（0.7）
   - LLM_TOP_P：采样概率（0.9）
   - LLM_MAX_TOKENS：最大生成长度（2000）
   - LLM_FREQUENCY_PENALTY：频率惩罚（0.0）
   - LLM_PRESENCE_PENALTY：存在惩罚（0.0）

3. 质量控制：
   - MAX_REVIEW_LENGTH：最大评价长度（1000）
   - MIN_REVIEW_LENGTH：最小评价长度（200）
   - MAX_RETRIES：最大重试次数（3）
   - QUALITY_THRESHOLD：质量阈值（0.8）
   - SENTIMENT_THRESHOLD：情感阈值（0.8）

## API 接口

### 1. 生成评价
```http
POST /generate_reviews
```

### 2. 增强评价
```http
POST /enhance_reviews
```

### 3. 检查评价质量
```http
POST /check_quality
```

### 4. 批量检查评价质量
```http
POST /check_quality_batch
```

### 5. 获取质量检查结果
```http
GET /quality_check_result/{task_id}
```

### 6. 获取支持的产品类别
```http
GET /categories
```

### 7. 获取评价统计信息
```http
GET /review_stats/{category}
```

### 8. 健康检查
```http
GET /health
```

## 项目结构

```
backend/
├── api/
│   ├── routes.py              # API 路由
│   ├── category_generators.py # 类别生成器
│   └── review_enhancer.py     # 评价增强器
├── models/
│   ├── data_model.py         # 数据模型
│   ├── category_prompts.py   # 类别提示词
│   └── check_prompt.py       # 质量检查提示词
├── utils/
│   ├── review_saver.py       # 评价保存
│   └── quality_check.py      # 质量检查
├── docs/
│   └── api.md               # API 文档
├── config.py                # 配置文件
└── main.py                 # 主程序
```

## 评价质量要求

1. 情感倾向置信度（sentiment_score）：
   - 范围：0-1
   - 要求：≥ 0.8

2. 质量置信度（quality_score）：
   - 范围：0-1
   - 要求：≥ 0.8

3. 评价内容要求：
   - 长度：200-300字
   - 包含具体使用体验
   - 包含优缺点分析
   - 符合用户背景特征

## 开发说明

1. 添加新的产品类别：
   - 在 `category_generators.py` 中添加新的生成器类
   - 在 `category_prompts.py` 中添加新的提示词模板
   - 在 `routes.py` 的 `get_categories` 中添加新类别

2. 自定义评价保存：
   - 修改 `review_saver.py` 中的保存逻辑
   - 调整 CSV 文件的字段和格式
   - 添加新的统计指标

3. 调整大模型参数：
   - 在 `config.py` 中修改相关配置
   - 在提示词模板中调整生成参数
   - 根据需要调整质量控制阈值

## 注意事项

1. API 密钥安全：
   - 不要在代码中硬编码 API 密钥
   - 使用环境变量或配置文件管理密钥
   - 定期轮换 API 密钥

2. 大模型使用：
   - 注意控制 API 调用频率
   - 合理设置生成参数
   - 监控 API 使用成本

3. 评价生成限制：
   - 单次最多生成 10 条评价
   - 生成失败会自动重试（最多 3 次）
   - 质量不达标会自动重新生成

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License