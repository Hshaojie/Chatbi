# NexusMind

**企业级 ChatBI Agent 平台** —— 基于多 Agent 编排、RAG 检索增强、长期记忆与发布门禁（Harness）的对话式数据分析系统。

用户用自然语言提问，系统自动完成意图识别 → 查询改写 → Schema 检索 → SQL 生成与校验 → 查询执行 → 图表/结论合成，并支持知识库问答、多轮会话恢复、权限治理、技能进化与可观测性。

---

## 功能特性

- **多 Agent 编排**：意图识别、查询改写、ReAct 推理、反思重试，多路径协同完成复杂问题。
- **ChatBI 能力**：语义层、Schema 检索、SQL AST 安全校验、数据质量检查、根因分析、混合知识检索。
- **RAG 知识库**：Milvus 向量检索 + bge-m3 嵌入 + bge-reranker 重排，支持文档上传、增量索引、索引一致性校验。
- **长期记忆**：对话自动提取与压缩、分层记忆存储（加密存档）、上下文预算管理与会话压缩。
- **企业治理**：基于角色的访问控制（ACL）、审计日志、租户与数据权限策略。
- **技能与自进化**：Skills 注册与调用、Bad Case 沉淀、进化闭环与人工审批。
- **发布门禁（Harness）**：版本化评测集、质量/延迟/成本/安全多维门禁、金丝雀发布与回滚。
- **可观测性**：OpenTelemetry 链路追踪、Prometheus 指标、Grafana 看板、Tempo + Alertmanager。
- **开箱即用**：Docker Compose 一键拉起 etcd / MinIO / Milvus / PostgreSQL / Redis / 后端 / 前端。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 后端 | Python 3.11+、FastAPI、LangGraph、LangChain、pymilvus、psycopg/asyncpg、Redis |
| 前端 | React 19 + TypeScript + Vite、ECharts |
| 存储 | Milvus（向量）、PostgreSQL（业务/检查点）、Redis（缓存/会话）、MinIO（对象存储） |
| 可观测性 | OpenTelemetry、Prometheus、Grafana、Tempo、Alertmanager |
| 部署 | Docker Compose、Nginx |

## 快速开始

### 1. 准备配置

```bash
cp .env.example .env      # Windows: Copy-Item .env.example .env
```

然后在 `.env` 中填写至少以下内容：

- `DASHSCOPE_API_KEY`：主模型 API Key（阿里云百炼 / DashScope）
- `EMBEDDING_API_KEY`：嵌入模型 API Key（SiliconFlow 等）
- `RERANK_API_KEY`：重排模型 API Key
- `POSTGRES_USER` / `POSTGRES_PASSWORD` / `DATABASE_URL`：数据库凭据

> 加密相关密钥（`GRAPH_CHECKPOINT_FERNET_KEY`、`CONTEXT_STORE_FERNET_KEY` 等）可留空，部署脚本会为首次初始化自动生成，且不会覆盖已有密钥。

### 2. 一键部署

```bash
python scripts/deploy.py --init   # 首次部署：生成密钥、准备数据目录
python scripts/deploy.py          # 启动整套服务
```

服务启动后：

- 前端：<http://localhost:5173>
- 后端 API 文档：<http://localhost:8000/docs>

### 3. 本地开发（不使用 Docker）

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate ; Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# 启动后端（在 backend 目录下）
cd backend && python main.py

# 启动前端
cd frontend && npm install && npm run dev
```

### 4. 命令行使用

```bash
python cli.py chat                 # 交互式对话（默认连 http://localhost:8000）
python cli.py chat --stream        # 流式对话
python cli.py chat --session-id x  # 恢复会话
python cli.py kb upload ./doc.pdf  # 上传文档到知识库
python cli.py test                 # 一键验证所有功能
```

## 测试

```bash
# 全量确定性单元测试（CI 使用的命令）
python -m unittest discover -s tests -p 'test*.py' -v

# 前端测试
cd frontend && npm test
```

仓库内置 GitHub Actions 工作流 `.github/workflows/harness.yml`，在 push / pull request 时自动执行测试门禁。

## 目录结构

```
.
├── backend/               # FastAPI 后端
│   ├── api.py, main.py    # 入口与路由
│   ├── chatbi/            # ChatBI：语义层、SQL 校验、根因分析
│   ├── core/              # 编排器、意图识别、查询改写、ReAct
│   ├── rag/               # 知识库、嵌入、Milvus、上传任务
│   ├── memory/            # 长期记忆、压缩、分层存储
│   ├── governance/        # 权限、策略、审计
│   ├── harness/           # 评测门禁、晋升、金丝雀
│   ├── evaluation/        # 评测、监控、自进化
│   ├── skills/, tools/    # 技能与工具（SQL、MCP）
│   └── infra/             # 配置、LLM Provider、数据库、检查点
├── frontend/              # React + TypeScript 前端
├── deploy/                # Nginx 与可观测性（Prometheus/Grafana/Tempo）配置
├── scripts/               # 部署、评测、验证脚本
├── tests/                 # 单元测试与集成验证
├── docker-compose*.yml    # 编排文件（默认 / 开发 / 生产 / 可观测性）
└── cli.py                 # 命令行客户端
```

## 配置说明

所有配置通过环境变量注入，完整清单见 `.env.example`。`.env` 已被 `.gitignore` 忽略，**请勿提交真实密钥**。

## 安全提示

- 仓库不包含任何生产密钥；CI 不读取 `.env`。
- `docker-compose.yml` 中的数据库密码仅用于本地开发，生产部署请通过密钥管理服务注入。
- 身份请求头模式（`NEXUSMIND_ALLOW_HEADER_IDENTITY`）仅建议在可信内网或开发环境启用。

## 许可证

本项目暂未声明开源许可证。如需开源，请补充 `LICENSE` 文件（如 MIT / Apache-2.0）。
