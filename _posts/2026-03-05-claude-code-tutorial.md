---
layout: post
title: Claude Code 用法速查手册
date: 2026-03-05
comments: true
toc: true
mathjax: false
categories: [ "claude-code" ]
---

## 一、安装与启动

### 1. 安装 Claude Code

Claude Code 提供多种安装方式，可根据平台和偏好选择：

#### 方式一：原生安装（推荐，无需 Node.js）

**macOS / Linux / WSL**：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)**：

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows (CMD)**：

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> 原生安装方式为独立可执行文件，无需 Node.js 依赖，支持自动更新。

#### 方式二：Homebrew（macOS / Linux）

```bash
brew install --cask claude-code
```

#### 方式三：npm（需要 Node.js 18+）

```bash
npm install -g @anthropic-ai/claude-code
```

> **注意**：避免使用 `sudo` 安装以防权限问题。

#### 验证安装

```bash
claude --version
claude doctor    # 运行诊断检查
```

### 2. 启动 Claude Code

```bash
claude
```

在项目目录下执行 `claude` 命令即可启动 Claude Code，进入交互式对话界面。

### 3. 跳过权限检测启动

```bash
claude --dangerously-skip-permissions
```

启动时加上该参数，Claude Code 将跳过所有权限检测（文件写入、终端命令执行等均不再询问）。启动后模式显示为 **bypass permissions on**。

> **警告**：官方在参数名中使用了 "dangerously"（危险地）一词，启用后 Claude Code 拥有与你相同的终端权限，理论上存在一定风险。

### 4. 恢复对话启动

**恢复最近的对话**：

```bash
claude -c
# 或者
claude --continue
```

`-c` 是 `continue` 的缩写，启动 Claude Code 并自动恢复上一次的对话会话。

**选择历史对话恢复**：

```bash
claude -r
# 或者
claude --resume
```

`-r` 是 `resume` 的缩写，启动后会显示交互式列表，允许你从之前的会话历史中选择一个进行恢复。

### 5. 更新 Claude Code

```bash
claude update
```

Claude Code 默认启用自动更新。若需禁用自动更新，可设置环境变量 `export DISABLE_AUTOUPDATER=1`。

## 二、交互模式（三种模式）

通过 **Shift + Tab** 在三种模式之间循环切换：

| 模式 | 标识 | 说明 |
|------|------|------|
| **默认模式** | 底部显示 `? for shortcuts` | 最谨慎，每次创建/修改文件前都会询问用户确认 |
| **自动模式** | 底部显示 `accept edits on` | 自动同意所有文件的创建和修改操作，不再逐次询问 |
| **规划模式** | 底部显示 `Plan Mode On` | 只讨论方案、不执行任何文件修改，适合构思和确认细节 |

### 权限确认选项

当 Claude Code 请求写入文件时，会提供三个选项：

1. **Yes** — 单次授权，仅同意当前这一次操作
2. **Yes, allow all edits during this session** — 本次会话期间自动同意所有文件操作
3. **No** — 拒绝，可继续输入修改意见

### 终端命令执行确认

即使在自动模式（accept edits on）下，执行终端命令（如 `mkdir`、`npm install`）仍会单独询问确认，因为 Claude Code 认为终端命令是较危险的操作。

## 三、输入与编辑

### 1. 换行输入

```
Shift + Enter
```

在输入框中换行（直接按 Enter 会提交请求）。

### 2. 使用 VSCode/vim 编辑输入

```
Ctrl + g
```

按下后会打开 VSCode/vim 标签页，可在其中更方便地编辑多行输入内容。编辑完成后保存并关闭标签页，内容会自动回填到 Claude Code 输入框。

### 3. 执行终端命令（Bash 模式）

在输入框中输入 **`!`**（叹号），即可进入 Bash 模式，直接运行任意终端命令。例如：

```
! open index.html
! ls
```

### 4. 查看完整输出

```
Ctrl + o
```

当输出内容被截断时（如文件列表只显示部分），按 `Ctrl + O` 可展开查看完整内容。也可用于查看压缩后的上下文内容。

### 5. 使用 `@` 引用文件或目录

在输入框中使用 `@` 符号可以精确引用项目中的文件或目录，让 Claude Code 只关注相关上下文，避免将整个项目都喂给 AI：

```
@src/auth.ts           # 引用单个文件
@src/components/       # 引用整个目录结构
@src/utils.ts 帮我重构这个文件
```

### 6. 管道输入

Claude Code 支持从管道读取输入，可配合 `-p` 参数使用，适合在脚本或工作流中集成：

```bash
git diff | claude -p "解释这些更改"
cat error.log | claude -p "分析这个错误日志"
```

## 四、斜杠命令（/ Commands）

### `/login`

主动触发登录流程。支持两种接入方式：
- **订阅制**：使用 Claude Pro / Max 会员
- **API Key**：按 Token 用量计费

### `/logout`

登出当前账号。

### `/help`

查看所有可用命令列表。

### `/resume`

恢复之前的历史对话。执行后会列出历史会话列表，选择对应会话即可恢复。

### `/rewind`

回滚操作。将代码和/或会话回退到之前的某个回滚点。也可通过按 **两下 ESC** 快速进入回滚界面。

回滚提供四个选项：
1. 回滚代码和会话
2. 只回滚会话
3. 只回滚代码
4. 放弃回滚

> **注意**：Claude Code 只能回滚它自己写入的文件，由终端命令（如 `mkdir`、`npm install`）生成的文件无法回滚。建议配合 Git 使用以实现精准回滚。

### `/compact`

压缩当前上下文。可以直接执行，也可在后面追加压缩策略（如"重点保留用户提出的需求"）。压缩后能减少 Token 消耗，提升性能。

```
/compact
/compact 重点保留用户提出的需求
```

### `/cost`

查看当前会话的 Token 消耗量与预估成本，帮助监控用量。

### `/model`

切换当前使用的模型。例如从 Sonnet 切换到 Opus，或切换到其他已配置的模型。

### `/clear`

清空所有上下文内容（比 `/compact` 更彻底）。适用于后续任务与之前上下文无关的场景。

### `/init`

自动生成 `CLAUDE.md` 文件。Claude Code 会根据当前项目情况生成一份项目说明文件。

### `/memory`

打开 `CLAUDE.md` 文件进行编辑。会列出两种级别供选择：
- **项目级别**：文件在当前项目目录中，对当前项目生效
- **用户级别**：文件在用户主目录中，对当前用户的所有项目生效

### `/mcp`

查看和管理已安装的 MCP（Model Context Protocol）工具。可以：
- 查看已安装的 MCP Server 列表
- 进行鉴权（Authenticate）
- 查看工具列表（View tools）

### `/hooks`

进入 Hook 配置界面，设置在特定时机自动执行的自定义逻辑。

### `/tasks`

查看当前正在运行的后台任务列表。在任务列表中按 **k** 可终止对应任务。

### `/skills`

查看当前已安装的 Agent Skill 列表。

### `/agents`

创建和管理 SubAgent（子代理）。选择后可以：
- 创建新的 Agent（Create new agent）
- 选择项目级别或用户级别
- 选择创建方式（Claude 初始化 / 手动创建）

### `/plugin`

进入插件管理器，包含三个功能：
- **Discover**：发现和安装新插件
- **Installed**：查看已安装的插件
- **Marketplaces**：浏览插件市场

### `/<skill-name>`

直接调用指定的 Agent Skill。例如：

```
/daily-report 写一份今天的总结
```

省去大模型意图识别的过程，直接由用户主动调用指定 Skill，结果更加可控。

## 五、快捷键速查

| 快捷键 | 功能 |
|--------|------|
| `Shift + Tab` | 在默认模式 → 自动模式 → 规划模式之间循环切换 |
| `Shift + Enter` | 输入框中换行 |
| `Ctrl + g` | 打开 VSCode 编辑器来编写输入内容 |
| `Ctrl + b` | 将当前正在运行的服务/命令放到后台运行 |
| `Ctrl + o` | 展开查看完整输出内容 / 查看压缩后的上下文 |
| `Ctrl + v` | 粘贴图片到输入框（macOS 下也是 Ctrl+V，不是 Cmd+V） |
| `Ctrl + c`（按两下） | 退出 Claude Code |
| `ESC`（按两下） | 快速进入回滚（/rewind）界面 |
| `ESC` | 退出当前子界面，返回输入框 |
| `!` | 进入 Bash 模式，执行终端命令 |

## 六、CLAUDE.md — 项目记忆文件

`CLAUDE.md` 是 Claude Code 每次启动时自动读取的配置/说明文件，用于告知 Claude Code 项目信息、用户偏好、注意事项等。

### 使用方式

1. 使用 `/init` 自动生成
2. 使用 `/memory` 打开编辑
3. 直接在文件管理器或编辑器中手动编辑

### 多层级记忆体系

Claude Code 的记忆文件支持多层级加载，优先级从高到低：

| 级别 | 文件位置 | 生效范围 |
|------|----------|----------|
| 企业级别 | 由管理员统一配置 | 对所有企业成员生效 |
| 用户级别 | `~/.claude/CLAUDE.md` | 对当前用户的所有项目生效 |
| 项目级别（共享） | 项目根目录下的 `CLAUDE.md` | 所有项目成员共享，可纳入版本管理 |
| 项目级别（本地） | 项目根目录下的 `CLAUDE.local.md` | 仅本机生效，不纳入版本管理 |
| 路径规则 | `.claude/rules/*.md` | 可通过 YAML frontmatter 指定作用于特定文件路径 |

> **路径规则示例**：在 `.claude/rules/api-style.md` 中通过 YAML frontmatter 指定 `globs: ["src/api/**/*.ts"]`，规则仅对匹配路径的文件生效。

### 自动记忆

Claude Code 还支持自动记忆功能：当你在对话中纠正 Claude 的行为时，可以要求它将纠正内容更新到 `CLAUDE.md`，避免下次重复犯错。Claude 每个会话最多可自动写入 200 行记忆笔记。

### 典型用途

- 项目技术栈说明
- 编码规范和注意事项
- 自定义回复要求（如每次回答末尾追加特定内容）
- 项目结构描述
- 常用构建/测试命令

### 示例内容

```markdown
# CLAUDE.md

## 常用命令
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## 代码规范
- 使用 TypeScript 和 React Hooks
- 组件文件名使用 PascalCase
- 所有的异步操作必须使用 try/catch

## 架构说明
- 状态管理使用 Zustand
- 样式使用 Tailwind CSS
- 路由使用 React Router v6
```

## 七、Hook — 自动化钩子

Hook 允许用户在 Claude Code 运行工具的前后等时机，自动执行自定义逻辑。

### 配置方式

**方式一：交互式配置（推荐）**

在 Claude Code 中输入 `/hooks` 命令，进入交互式配置界面，按提示选择事件类型、匹配器和命令即可。配置完成后会自动写入对应的 JSON 文件。

**方式二：手动编辑 JSON 配置文件**

Hook 配置存储在 Claude Code 的 `settings.json` 文件中（与权限等其他设置共用同一文件），根据生效范围不同，文件位于以下路径：

| 生效范围 | 配置文件路径 | 说明 |
|----------|-------------|------|
| 用户全局 | `~/.claude/settings.json` | 对当前用户所有项目生效 |
| 项目共享 | `<项目根目录>/.claude/settings.json` | 可纳入 Git 版本管理，团队共享 |
| 项目本地 | `<项目根目录>/.claude/settings.local.json` | 自动被 `.gitignore` 忽略，仅本机生效 |

在对应文件中添加 `"hooks"` 字段即可：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs prettier --write"
          }
        ]
      }
    ]
  }
}
```

> **提示**：如果文件中已有其他配置（如 `permissions` 等），只需在 JSON 对象中追加 `"hooks"` 字段，与其他配置同级即可。

Hook 类型支持 `"command"`（执行 bash 命令）和 `"prompt"`（交由 LLM 评估判断）两种。

### 执行时机

| 时机 | 说明 |
|------|------|
| **PreToolUse** | 工具使用前（可批准/拒绝/修改输入） |
| **PostToolUse** | 工具使用后（可验证结果、自动格式化等） |
| **Notification** | 发送通知时（如转发到 Slack/邮件） |
| **UserPromptSubmit** | 用户提交 Prompt 前（可验证/修改/注入上下文） |
| **Stop** | 主 Agent 完成响应时（可阻止停止以继续执行） |
| **SubagentStop** | SubAgent 完成时（处理子代理返回结果） |
| **SessionStart** | 会话启动或恢复时（注入环境变量/初始上下文） |

> **注意**：原有的 `ToolUseError` 事件已被移除，错误处理建议在 `PostToolUse` 中通过返回 `"decision": "block"` 来实现。

### 匹配工具

可指定触发 Hook 的工具类型（matcher），支持多种匹配方式：
- **精确匹配**：`Write`、`Edit`（区分大小写）
- **正则匹配**：`Edit|Write`
- **通配符**：`*`（匹配所有工具）
- **MCP 工具**：`mcp__<server>__<tool>`（如 `mcp__filesystem__read_file`）

### 配置优先级

多个级别的 Hook 配置会同时生效（合并而非覆盖），执行顺序为：

1. **用户全局** (`~/.claude/settings.json`) — 最先加载
2. **项目共享** (`.claude/settings.json`) — 其次加载
3. **项目本地** (`.claude/settings.local.json`) — 最后加载

> 如果同一事件在多个级别都配置了 Hook，它们会**全部执行**，而非互相覆盖。

### 示例：自动格式化

在 `PostToolUse`（write/edit 之后）执行 prettier 格式化：

```bash
jq -r '.tool_input.file_path' | xargs prettier --write
```

工作流程：Claude Code 写入文件 → Hook 触发 → `jq` 从传入的 JSON 中提取文件路径 → `prettier` 格式化该文件。

## 八、多模态 — 图片输入

Claude Code 支持接收图片（如设计稿）作为输入：

### 方法一：拖拽

直接将图片文件拖入 Claude Code 终端窗口。

### 方法二：粘贴

1. 复制图片文件
2. 在 Claude Code 中按 **Ctrl + V** 粘贴

> **注意**：macOS 下也必须使用 `Ctrl + V`，而不是 `Cmd + V`。

## 九、MCP — 外部工具集成

MCP（Model Context Protocol）是大模型与外界沟通的渠道，可接入外部服务的 MCP Server 来扩展 Claude Code 的能力。

### 使用流程（以 Figma 为例）

1. 按照官方要求执行安装命令安装 MCP Server
2. 重启 Claude Code
3. 执行 `/mcp` 查看已安装的 MCP
4. 选择对应 MCP → Authenticate 完成鉴权
5. 在对话中提需求，Claude Code 会自动识别并调用合适的 MCP 工具

### 管理命令

```
/mcp              # 查看和管理 MCP Server
/mcp → View tools # 查看某个 MCP Server 的工具列表
```

## 十、Agent Skill — 自定义技能

Agent Skill 是一个给大模型看的动态加载的说明书（Prompt），用于定义特定场景下的行为规范。

### 创建方式

Skill 支持用户级和项目级两种存放位置：
- **用户级别**：`~/.claude/skills/<skill-name>/SKILL.md`（对当前用户所有项目生效）
- **项目级别**：`.claude/skills/<skill-name>/SKILL.md`（对当前项目生效）

创建步骤：
1. 在上述目录创建 `<skill-name>/` 文件夹
2. 在该文件夹中创建 `SKILL.md` 文件
3. 编写 Skill 内容（包含 name、description 和具体描述）
4. 可选：添加辅助脚本或模板文件（如 `fill_form.py`）以执行确定性操作

### SKILL.md 结构

```markdown
---
name: daily-report
description: 写每日总结时使用此 Skill
---

## 格式要求
- 日期
- 开发摘要
- 开发详情
...
```

### 调用方式

- **自动调用**：Claude Code 根据用户请求自动识别并调用匹配的 Skill
- **手动调用**：输入 `/<skill-name>` 直接调用（如 `/daily-report`）

### 查看已安装 Skill

```
/skills
```

## 十一、SubAgent — 子代理

SubAgent 是一个拥有独立上下文、独立工具的独立 Agent，可独立完成特定任务。

### 创建方式

**交互式创建**：
1. 输入 `/agents`
2. 选择 "Create new agent"
3. 选择级别（项目级别 / 用户级别）
4. 选择创建方式（Claude 初始化 / 手动创建）
5. 描述 Agent 要做的事情
6. 选择可用工具（如 Read-only tools）
7. 选择模型（如 Sonnet）
8. 选择展示颜色

**手动创建**：在以下目录放置配置文件：
- 用户级别：`~/.claude/agents/<agent-name>.md`
- 项目级别：`.claude/agents/<agent-name>.md`

### 内置 SubAgent

Claude Code 内置了几种 SubAgent：
- **Explore**：快速代码搜索和分析（使用 Haiku 模型，只读工具）
- **Plan**：面向复杂任务的研究和规划
- **通用型**：具有完整工具访问权限的多步骤任务处理

### Agent Skill vs SubAgent

| 对比维度 | Agent Skill | SubAgent |
|----------|-------------|----------|
| 上下文 | 共享主对话上下文 | 拥有独立上下文 |
| 中间过程 | 所有日志和思考过程记入主对话 | 中间过程不回传，只返回最终结果 |
| Token 影响 | 会增加主对话的 Token 消耗 | 不影响主对话 Token |
| 适用场景 | 与上下文关联大、对上下文影响小的任务（如写每日总结） | 与上下文关联小、对上下文影响大的任务（如代码审核） |

## 十二、Plugin — 插件系统

Plugin 是一个全家桶安装包，将 Skill、SubAgent、Hook、MCP 等能力打包在一起，一键安装。

### 管理命令

```
/plugin
```

### 功能面板

| 选项 | 说明 |
|------|------|
| **Discover** | 发现和安装新插件 |
| **Installed** | 查看已安装的插件 |
| **Marketplaces** | 浏览插件市场 |

### 安装范围

| 范围 | 说明 |
|------|------|
| 当前用户 | 对当前用户的所有项目生效 |
| 当前项目 | 对当前项目的所有用户生效 |
| 当前用户 + 当前项目 | 仅对当前用户在当前项目中生效 |

### 示例

安装 `frontend-design` 插件后，Claude Code 获得 Anthropic 官方沉淀的 UI 设计能力，生成的前端界面排版更高级、色彩更协调、交互更符合现代审美。

## 十三、后台任务管理

### 将运行中的服务放到后台

```
Ctrl + b
```

当一个服务（如 `npm run dev`）正在运行并阻塞 Claude Code 时，按 `Ctrl + b` 可将其放到后台，继续与 Claude Code 交互。

### 查看后台任务

```
/tasks
```

### 终止后台任务

在 `/tasks` 界面中按 **k** 终止对应任务。

## 十四、Plan Mode — 规划模式详解

Plan Mode 适合在动手之前先讨论方案、确认细节。

### 进入方式

按 `Shift + Tab` 切换到 Plan Mode（底部显示 `Plan Mode On`）。

### 工作流程

1. 进入 Plan Mode
2. 输入需求，Claude Code 生成详细计划（包含目标、项目清单、目录结构等）
3. 审核计划，有三个选项：
   - **执行计划 + 进入自动模式**：开始执行，后续文件操作不再询问
   - **执行计划 + 默认模式**：开始执行，每次写入文件前仍需确认
   - **继续修改计划**：输入修改意见，Claude Code 重新生成计划

## 十五、环境变量与模型配置

Claude Code 本身不与 Claude 模型绑定，可通过设置环境变量使用其他模型（如 DeepSeek、通义千问 Qwen、GLM、MiniMax 等）来驱动。

### 配置方式

**macOS / Linux**（添加到 `~/.bashrc` 或 `~/.zshrc`）：

```bash
# DeepSeek 示例
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=sk-your-deepseek-key
export ANTHROPIC_MODEL=deepseek-chat

# 阿里云百炼 (Qwen) 示例
export ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
export ANTHROPIC_API_KEY=sk-your-qwen-key
export ANTHROPIC_MODEL=qwen3-coder-plus
```

**Windows (PowerShell)**：

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_API_KEY="sk-your-deepseek-key"
$env:ANTHROPIC_MODEL="deepseek-chat"
```

### 关键环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_BASE_URL` | 模型 API 的基础 URL（替换为第三方兼容接口地址） |
| `ANTHROPIC_API_KEY` | 对应模型服务商的 API Key（推荐使用） |
| `ANTHROPIC_MODEL` | 使用的模型名称 |

### 关于 API Key 变量名的区别

在配置过程中，你可能会遇到 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 两种写法，它们的区别如下：

*   **`ANTHROPIC_API_KEY`**：这是 Anthropic SDK 的**标准变量名**，用于直接与 Anthropic API 或第三方兼容模型通信。如果此变量设置为非空值，Claude Code 会优先使用它进行认证。
*   **`ANTHROPIC_AUTH_TOKEN`**：这是用于特定网关（如 Vercel AI Gateway）或 Claude Code CLI 登录后自动生成的认证令牌。使用此变量时，需要将 `ANTHROPIC_API_KEY` 显式设置为空字符串 `""`。

**最佳实践**：
*   两者**并非等价**，`ANTHROPIC_API_KEY` 优先级高于 `ANTHROPIC_AUTH_TOKEN`。
*   **切勿同时设置两者**：否则可能触发 `Auth conflict` 错误（特别是在 Windows 上）。如遇冲突，需删除所有相关环境变量并清除 `~/.claude` 缓存后重新登录。
*   **推荐**：直接使用 API 或第三方模型时优先用 **`ANTHROPIC_API_KEY`**；使用网关代理时用 **`ANTHROPIC_AUTH_TOKEN`** 并将 `ANTHROPIC_API_KEY` 设为空。

## 十六、最佳实践 Tips

### 核心原则

1. **提供明确的验证标准**：始终为 Claude 提供可验证的标准（如测试用例、预期输出或设计截图），让其能够自我检查并修正错误。避免模糊指令如"修复登录问题"，应改为"检查 `src/auth/` 中的令牌刷新逻辑，编写失败测试并修复"。
2. **"先探索，再规划，后执行"**：对于复杂任务，推荐三步走策略——先让 Claude 探索代码库了解现状，再进入 Plan Mode 输出方案，确认后再执行。
3. **精确引用上下文**：不要把整个项目都喂给 AI。使用 `@文件名` 只引用相关文件，或者用 `!git diff` 只提供变更部分，节省 Token 并提升回答质量。

### 效率提升

1. **善用 Plan Mode**：在进行大规模重构或复杂功能开发前，先按 `Shift + Tab` 进入 Plan Mode，让 Claude Code 输出完整计划，确认无误后再执行。
2. **git worktree 并行开发**：使用 `git worktree` 创建多个独立工作目录，在不同终端标签页同时运行多个 Claude Code 会话，实现并行处理多个独立任务。
3. **定期清理上下文**：当任务完成后，使用 `/clear` 或 `/compact` 清理上下文，避免 Token 浪费和上下文干扰。连续两次纠正无效时，应重启会话并优化初始提示。
4. **管道集成工作流**：善用管道操作（如 `git diff | claude -p "解释这些更改"`），将 Claude Code 融入现有开发流程。

### 项目管理

1. **善用 CLAUDE.md**：将项目规范、常用命令、架构说明写入 `CLAUDE.md`，让 Claude Code 每次启动就了解项目全貌，减少重复沟通。每次纠正 Claude 的错误后，建议要求其更新 `CLAUDE.md` 以避免重复问题。注意 `CLAUDE.md` 不宜过长（建议不超过 200 行），定期精简。
2. **SubAgent 处理重型任务**：对于代码审核、全项目扫描等上下文消耗大的任务，使用 SubAgent 而非 Agent Skill，避免主对话上下文被撑爆。对简单的搜索/分析任务，可使用 Haiku 模型的 SubAgent 以降低成本。
3. **配合 Git 使用**：不要过度依赖 `/rewind` 回滚功能，结合 Git 进行版本管理更为精准可靠。

### 安全与权限

1. **合理使用危险模式**：`claude --dangerously-skip-permissions` 适合在沙盒环境或对 AI 充分信任时使用，实现全自动开发，但生产环境建议谨慎。
2. **善用 Hook 自动化**：通过配置 `PostToolUse` Hook 自动执行代码格式化、lint 检查等，通过 `PreToolUse` Hook 拦截危险操作（如 `rm -rf`），提升开发安全性与一致性。

## 附录：命令速查表

| 命令/操作 | 功能 |
|-----------|------|
| `claude` | 启动 Claude Code |
| `claude -c` | 启动并恢复上次对话 |
| `claude -p "prompt"` | 管道模式，接收标准输入并处理 |
| `claude --dangerously-skip-permissions` | 跳过所有权限检测启动 |
| `claude update` | 手动更新 Claude Code |
| `claude doctor` | 运行诊断检查 |
| `claude --version` | 查看当前版本 |
| `/login` | 登录 |
| `/logout` | 登出 |
| `/help` | 查看所有可用命令 |
| `/resume` | 恢复历史对话 |
| `/rewind` 或 `ESC ESC` | 回滚 |
| `/compact` | 压缩上下文 |
| `/clear` | 清空上下文 |
| `/cost` | 查看 Token 消耗与成本 |
| `/model` | 切换模型 |
| `/init` | 生成 CLAUDE.md |
| `/memory` | 编辑 CLAUDE.md |
| `/mcp` | 管理 MCP 工具 |
| `/hooks` | 配置 Hook |
| `/tasks` | 查看后台任务 |
| `/skills` | 查看 Agent Skill |
| `/agents` | 管理 SubAgent |
| `/plugin` | 管理插件 |
| `/<skill-name>` | 直接调用指定 Skill |
| `!<command>` | 执行终端命令 |
| `@<file/dir>` | 引用文件或目录 |
| `Shift + Tab` | 切换模式 |
| `Shift + Enter` | 换行 |
| `Ctrl + g` | 用 VSCode 编辑输入 |
| `Ctrl + b` | 将服务放到后台 |
| `Ctrl + o` | 展开完整输出 |
| `Ctrl + v` | 粘贴图片 |
| `Ctrl + c`（按两下） | 退出 Claude Code |
| `ESC`（按两下） | 进入回滚界面 |
| `ESC` | 返回输入框 |
| `!` | 进入 Bash 模式 |