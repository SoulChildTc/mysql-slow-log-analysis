# MySQL 慢日志分析平台

这是一个基于 Flask 的 Web 应用程序，用于分析 MySQL 慢查询日志。该工具使用 pt-query-digest 来处理慢查询日志，并提供了一个直观的 Web 界面来可视化分析结果。

## 功能特点

- 上传并分析 MySQL 慢查询日志文件
- 可视化展示查询性能数据，包括查询时间分布、查询次数分布等
- 显示全局统计信息和慢查询
- 提供所有查询的详细列表，支持按数据库筛选
- 查看完整的 SQL 查询语句，并提供语法高亮
- 支持历史分析记录的保存和查看

## 技术栈

- 后端：Flask (Python)
- 前端：HTML, CSS, JavaScript
- 数据可视化：Chart.js
- 数据表格：DataTables
- SQL 格式化和高亮：sql-formatter, highlight.js

## 快速开始

本项目提供了 Dockerfile，可以轻松构建 Docker 镜像, 您也可以直接使用已构建的 Docker 镜像：

```bash
docker run -d -p 5000:5000 ghcr.io/soulchildtc/mysql-slow-log-analysis:latest
```

## 项目结构

```bash
.
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖列表
├── Dockerfile          # Docker 构建文件
├── fe/                 # 前端文件目录
│   ├── index.html      # 主页面
│   └── index-v1.html   # 备用页面
└── README.md           # 项目说明文档
```

## 注意事项

- 请确保上传的日志文件格式正确，且不包含敏感信息。
- 大型日志文件的分析可能需要较长时间，请耐心等待。
- 本工具仅用于分析目的，不会修改原始日志文件或数据库。

## AI 开发声明

本项目完全由人工智能开发，展示了AI在软件开发领域的能力和潜力。

## 贡献

欢迎提交 Issues 和 Pull Requests 来改进这个项目。

## 许可证

[MIT License](LICENSE)
