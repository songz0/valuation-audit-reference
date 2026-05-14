"""
NotebookLM 知识库查询脚本 — valuation-audit-reference Skill 辅助工具

用途：在审计流程中查询用户的 NotebookLM 专业知识库（CPA/CFA/资产评估/审计文库/法规库），
      获取 checklist 不覆盖的准则条文、行业基准、方法论细节。

底层依赖：notebooklm-py >= 0.4.0 (https://github.com/teng-lin/notebooklm-py)

调用方式：
  python query_knowledge_base.py "查询问题"
  python query_knowledge_base.py "查询问题" --notebook <notebook_id>
  python query_knowledge_base.py "查询问题" --timeout 120
  python query_knowledge_base.py "查询问题" --json          # 结构化输出（含引用源）
  python query_knowledge_base.py "查询问题" --profile myprofile

默认 notebook：741b07fd-fa59-4ee3-bcf7-e83d530b2068（"工作"）
"""

import subprocess
import sys
import os
import argparse
import json

PYTHON = os.path.join(os.path.dirname(sys.executable), "python.exe") if os.name == "nt" else sys.executable
DEFAULT_NOTEBOOK = "741b07fd-fa59-4ee3-bcf7-e83d530b2068"
DEFAULT_TIMEOUT = 150  # seconds — NotebookLM 响应约 80-90s


def query(
    question: str,
    notebook_id: str = DEFAULT_NOTEBOOK,
    timeout: int = DEFAULT_TIMEOUT,
    as_json: bool = False,
    profile: str | None = None,
) -> str:
    """向 NotebookLM 发送查询并返回答案文本（或 JSON 字符串）。

    v0.4.0 新增:
      --json      结构化输出，含 references/source_id
      --profile   多 profile 支持
    """
    cmd = [
        PYTHON, "-m", "notebooklm", "ask", question,
        "-n", notebook_id,
    ]
    if as_json:
        cmd.append("--json")
    if profile:
        cmd.extend(["--profile", profile])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            error_msg = result.stderr.strip() or output
            return f"[KB 查询失败] returncode={result.returncode}\n{error_msg}"

        if as_json:
            # 直接返回 JSON 字符串供调用方解析
            return output

        # 纯文本模式：提取 Answer: 之后的内容
        if "Answer:" in output:
            answer = output.split("Answer:", 1)[1].strip()
            lines = answer.split("\n")
            clean_lines = [l for l in lines if not l.startswith("Resumed conversation:")]
            return "\n".join(clean_lines).strip()
        return output
    except subprocess.TimeoutExpired:
        return f"[KB 查询超时] 超过 {timeout}s 未返回。请稍后重试或缩短问题。"


def main():
    parser = argparse.ArgumentParser(description="查询 NotebookLM 专业知识库")
    parser.add_argument("question", help="查询问题")
    parser.add_argument("--notebook", default=DEFAULT_NOTEBOOK, help="NotebookLM notebook ID")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="超时秒数")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="返回 JSON 格式（含源引用）")
    parser.add_argument("--profile", default=None,
                        help="NotebookLM profile 名称（多账号场景）")
    args = parser.parse_args()

    answer = query(args.question, args.notebook, args.timeout,
                   as_json=args.as_json, profile=args.profile)
    print(answer)


if __name__ == "__main__":
    main()
