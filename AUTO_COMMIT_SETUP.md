# 硅基世界 2 - 自动提交配置指南

## 📋 已创建的文件

1. **auto-commit.bat** - Windows 批处理自动提交脚本
2. **auto-commit-daily.ps1** - PowerShell 自动提交脚本（支持定时任务）

## 🚀 使用方法

### 方法一：手动运行（推荐）

每次需要提交时运行：

```bash
# 在项目目录下运行
.\auto-commit.bat
```

或

```powershell
.\auto-commit-daily.ps1 -RunNow
```

### 方法二：设置 Windows 定时任务

#### 使用 PowerShell 脚本（需要管理员权限）

```powershell
# 以管理员身份运行 PowerShell
.\auto-commit-daily.ps1 -Setup
```

#### 使用图形界面手动创建

1. 打开 **任务计划程序** (taskschd.msc)
2. 点击 **创建基本任务**
3. 名称：`SiliconWorld2-DailyCommit`
4. 触发器：选择 **每天**
5. 时间：建议设置为 **凌晨 2:00**
6. 操作：选择 **启动程序**
7. 程序/脚本：
   ```
   C:\Windows\System32\cmd.exe
   ```
8. 添加参数：
   ```
   /c "cd /d C:\Users\97RPZ8T\.openclaw\workspace\silicon-world-2 && auto-commit.bat"
   ```
9. 完成

### 方法三：使用 Git Hooks（每次 commit 前自动推送）

在项目目录下创建 `.git/hooks/post-commit` 文件：

```bash
#!/bin/bash
git push origin main
```

然后赋予执行权限：

```bash
chmod +x .git/hooks/post-commit
```

## 📝 其他命令

```powershell
# 查看定时任务状态
.\auto-commit-daily.ps1 -Status

# 删除定时任务
.\auto-commit-daily.ps1 -Remove

# 立即执行一次提交
.\auto-commit-daily.ps1 -RunNow
```

## ⚙️ 配置选项

编辑 `auto-commit-daily.ps1` 可修改：

- `$taskTime` - 执行时间（默认 "02:00"）
- `$commitMsg` 格式 - 提交消息格式

## 🔍 日志查看

提交日志会显示在：
- 命令行输出
- Windows 事件查看器 -> 任务计划程序 -> 任务历史记录

## 📊 当前提交记录

查看最近的提交：

```bash
git log --oneline -10
```

## ✅ 最佳实践

1. **每天至少提交一次** - 保持代码新鲜
2. **提交前检查** - 确保没有敏感信息
3. **网络检查** - 确保能访问 GitHub
4. **定期查看** - 确认定时任务正常运行

## 🛠️ 故障排除

### 问题：git push 失败

**原因**：网络问题或 GitHub 不可访问

**解决**：
- 检查网络连接
- 手动运行 `git push` 测试
- 检查 GitHub 状态

### 问题：定时任务不执行

**原因**：权限问题或计算机休眠

**解决**：
- 以管理员身份运行任务计划程序
- 在任务属性中勾选 "唤醒计算机运行此任务"
- 检查任务历史记录

### 问题：中文乱码

**解决**：
- 确保使用 UTF-8 编码保存脚本
- 在批处理文件开头添加 `chcp 65001`

---

**最后更新**: 2026-04-07
**项目**: 硅基世界 2 (guiji-shijie-2)
