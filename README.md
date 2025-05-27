# AI代码评审API

## 项目结构

详见 `功能方案设计.md`。

## 启动方式



```bash
conda activate ai_code_review
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir ai_code_review_api
``` 