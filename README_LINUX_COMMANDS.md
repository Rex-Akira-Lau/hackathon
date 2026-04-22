

---

## 附录：Linux各发行版基础操作整理

### 说明

绝大多数Linux发行版核心基础操作通用，差异主要集中在包管理器（软件安装/更新）和部分系统配置命令，以下分通用部分和各发行版独特部分整理，命令可直接复制使用。

### 一、通用基础操作（所有Linux发行版通用）

#### 1. 文件与目录操作（核心高频）

**ls - 列出目录内容**
```bash
ls                      # 简单列出当前目录文件/文件夹
ls -l                   # 详细列出（包含权限、大小、修改时间等）
ls -a                   # 显示隐藏文件（以.开头的文件）
ls -lh                  # 人性化显示文件大小（KB/MB/GB）
```

**cd - 切换工作目录**
```bash
cd /home                # 通过绝对路径切换到/home目录
cd ..                   # 切换到上级目录
cd ~                    # 切换到当前用户的家目录
cd -                    # 切换到上一次所在的目录
```

**pwd - 显示当前所在的绝对路径**
```bash
pwd                     # 显示当前目录的绝对路径
```

**mkdir - 创建目录**
```bash
mkdir test              # 创建单个名为test的目录
mkdir -p a/b/c          # 递归创建多层目录（a目录下的b目录，b目录下的c目录）
```

**rm - 删除文件/目录（慎用！）**
```bash
rm file.txt             # 删除单个文件
rm -r dir/              # 递归删除目录及目录内所有内容
rm -rf dir/             # 强制、无提示删除目录及内容（高危命令，避免误删系统文件）
```

**cp - 复制文件/目录**
```bash
cp a.txt b.txt           # 将a.txt复制为b.txt（同目录）
cp -r dir1/ dir2/        # 递归复制dir1目录及内容到dir2目录
```

**mv - 移动文件/目录，或重命名**
```bash
mv a.txt b.txt           # 将a.txt重命名为b.txt
mv file.txt /tmp/        # 将file.txt移动到/tmp目录下
```

**文件查看命令**
```bash
cat file.txt             # 一次性显示文件所有内容（适合小文件）
less file.log            # 分页查看文件（空格翻页、回车下移一行、q退出）
head -20 file            # 查看文件前20行
tail -f log.txt          # 实时跟踪文件末尾内容（适合查看日志，ctrl+c退出）
```

#### 2. 权限与用户操作

**chmod - 修改文件/目录权限**
```bash
chmod 755 file.sh        # 设置权限为rwxr-xr-x（所有者可读写执行，其他只读）
chmod +x file.sh         # 给文件添加执行权限（常用于脚本运行）
```

**chown - 修改文件/目录的所有者和所属组**
```bash
chown user:group file.txt   # 将file.txt的所有者改为user，所属组改为group
```

**sudo - 以管理员（root）权限执行命令**
```bash
sudo ls /root            # 以root权限查看/root目录内容
```

**su - 切换用户**
```bash
su root                   # 切换到root用户（需输入root密码）
su - user                # 切换到user用户，并加载该用户的环境变量
```

#### 3. 进程与系统监控

**ps - 查看系统进程**
```bash
ps aux                   # 查看所有进程的详细信息（用户、PID、占用资源等）
```

**top/htop - 实时监控系统资源和进程**
```bash
top                      # 实时监控系统资源（q退出）
htop                     # 需额外安装，更友好的交互式界面
```

**kill - 终止进程**
```bash
kill 1234                # 通过PID（1234）正常终止进程
kill -9 1234             # 强制终止进程（无法正常终止时使用）
```

**系统资源查看**
```bash
df -h                    # 查看磁盘分区使用情况（人性化显示大小）
du -sh dir/              # 查看指定目录的总大小
free -h                  # 查看内存使用情况（总内存、已用、空闲）
```

#### 4. 网络基础操作

**ping - 测试网络连通性**
```bash
ping baidu.com           # 测试与百度的连通性（ctrl+c停止）
```

**ifconfig/ip a - 查看网卡信息**
```bash
ifconfig                 # 部分系统需安装net-tools工具
ip a                     # 更现代的命令，推荐使用
```

**ss/netstat - 查看端口和网络连接**
```bash
ss -tuln                 # 查看所有监听中的TCP/UDP端口
netstat -tuln            # 需安装net-tools
```

**curl - 发送HTTP请求**
```bash
curl baidu.com           # 获取百度首页内容
```

#### 5. 其他通用命令

```bash
clear                    # 清空终端屏幕
history                  # 查看终端执行过的历史命令
man 命令                 # 查看命令的帮助文档（如man ls）
reboot                   # 重启系统（需sudo权限）
shutdown -h now          # 立即关机（需sudo权限）
```

### 二、各发行版独特操作（核心差异：包管理器+部分系统命令）

> 以下仅列出各发行版独有/差异较大的命令，通用命令参考第一部分。

#### 1. Debian 系列（Debian、Ubuntu、Linux Mint、Kali Linux、Deepin、统信UOS）

**核心：包管理器 apt（.deb格式软件）**

```bash
# 更新软件源（获取最新软件列表）
sudo apt update

# 安装软件
sudo apt install nginx

# 卸载软件
sudo apt remove nginx          # 保留配置文件
sudo apt purge nginx           # 彻底卸载，删除配置文件

# 升级所有已安装软件
sudo apt upgrade

# 清理软件缓存
sudo apt clean

# 安装.deb格式本地软件
sudo dpkg -i 软件包.deb
# 若依赖缺失，修复命令
sudo apt -f install
```

**其他独特命令**
```bash
# Ubuntu 切换软件源（图形化）
software-properties-gtk

# Kali Linux 更新系统
sudo apt update && sudo apt full-upgrade -y

# 防火墙操作（Ubuntu默认使用ufw）
sudo ufw status               # 查看防火墙状态
sudo ufw allow 80/tcp         # 允许80端口
sudo ufw deny 22/tcp          # 拒绝22端口
sudo ufw enable               # 启用防火墙
```

#### 2. RHEL 系列（RHEL、CentOS、Fedora、AlmaLinux、Rocky Linux、Oracle Linux、Amazon Linux）

**核心：包管理器 dnf/yum（.rpm格式软件）**

> 注：CentOS 7 及以下用 yum，CentOS 8+、Fedora、RHEL 8+ 用 dnf（dnf 是 yum 的升级版本）

```bash
# 更新软件源
sudo dnf check-update         # dnf 系统
sudo yum check-update          # yum 系统

# 安装软件
sudo dnf install nginx        # dnf 系统
sudo yum install nginx         # yum 系统

# 卸载软件
sudo dnf remove nginx          # dnf 系统
sudo yum remove nginx          # yum 系统

# 升级所有已安装软件
sudo dnf upgrade               # dnf 系统
sudo yum update                # yum 系统

# 安装.rpm格式本地软件
sudo rpm -ivh 软件包.rpm
# 若依赖缺失，修复命令（dnf）
sudo dnf install -y 依赖包
```

**其他独特命令**
```bash
# CentOS 7 关闭防火墙（临时）
sudo systemctl stop firewalld

# CentOS 7 禁用防火墙（永久）
sudo systemctl disable firewalld

# Fedora 升级系统版本
sudo dnf system-upgrade download --releasever=新版本号
sudo dnf system-upgrade reboot

# 防火墙操作（RHEL/CentOS/Fedora使用firewalld）
sudo firewall-cmd --state              # 查看防火墙状态
sudo firewall-cmd --list-all            # 查看所有规则
sudo firewall-cmd --add-port=80/tcp     # 允许80端口
sudo firewall-cmd --remove-port=22/tcp # 拒绝22端口
sudo firewall-cmd --reload             # 重载规则
```

#### 3. SUSE 系列（openSUSE、SUSE Linux Enterprise）

**核心：包管理器 zypper（.rpm格式软件）**

```bash
# 更新软件源
sudo zypper refresh

# 安装软件
sudo zypper install nginx

# 卸载软件
sudo zypper remove nginx

# 升级所有已安装软件
sudo zypper update

# 搜索软件
sudo zypper search nginx

# 安装本地.rpm软件
sudo zypper install /path/to/package.rpm
```

**其他独特命令**
```bash
# 防火墙操作（使用firewalld）
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=80/tcp
sudo firewall-cmd --reload
```

#### 4. Arch Linux 系列（Arch Linux、Manjaro、EndeavourOS、Garuda Linux）

**核心：包管理器 pacman（.pkg.tar.zst格式软件）**

```bash
# 更新软件源和系统（同步并升级所有软件）
sudo pacman -Syu

# 安装软件
sudo pacman -S nginx

# 卸载软件（保留依赖）
sudo pacman -R nginx

# 卸载软件及依赖（彻底删除）
sudo pacman -Rs nginx

# 清理软件缓存
sudo pacman -Sc              # 清理旧缓存
sudo pacman -Scc             # 清理所有缓存

# 搜索软件
pacman -Ss nginx

# 安装本地软件包
sudo pacman -U 软件包.pkg.tar.zst
```

**其他独特命令**
```bash
# Manjaro 图形化包管理
pamac-manager

# Arch Linux 安装AUR仓库软件（需先安装yay）
yay -S 软件名

# 防火墙操作（Arch默认不安装防火墙，需手动配置）
sudo ufw status
sudo ufw allow 80/tcp
```

#### 5. Gentoo 系列（Gentoo Linux、Funtoo）

**核心：包管理器 emerge（.ebuild格式软件）**

```bash
# 同步Portage树
sudo emerge --sync

# 安装软件
sudo emerge nginx

# 卸载软件
sudo emerge --deselect nginx

# 升级所有已安装软件
sudo emerge -uDN @world

# 搜索软件
sudo emerge --search nginx

# 清理软件缓存
sudo eclean

# 修复依赖
sudo emerge --depclean
```

**服务管理（使用OpenRC）**
```bash
sudo rc-service nginx start       # 启动服务
sudo rc-service nginx stop        # 停止服务
sudo rc-service nginx restart     # 重启服务
sudo rc-update add nginx default  # 设置开机自启
sudo rc-update del nginx default  # 取消开机自启
rc-update show                    # 查看所有服务状态
```

#### 6. Slackware 系列（Slackware Linux）

**核心：包管理器 sbopkg/slackpkg（.tgz格式软件）**

```bash
# 更新软件包列表
sudo slackpkg update

# 安装软件
sudo slackpkg install-package nginx

# 卸载软件
sudo slackpkg remove-package nginx

# 升级所有已安装软件
sudo slackpkg upgrade-all

# 搜索软件
sudo slackpkg search nginx

# 安装本地软件包
sudo installpkg nginx.tgz
```

**服务管理（使用rc.d脚本）**
```bash
sudo /etc/rc.d/rc.local start     # 启动服务
sudo /etc/rc.d/rc.local stop      # 停止服务
sudo chmod +x /etc/rc.d/rc.local  # 设置开机自启
```

### 三、补充说明

#### 1. 服务管理

所有现代Linux发行版（无论哪个系列），均使用systemctl命令管理服务（通用），如：

```bash
sudo systemctl start nginx        # 启动服务
sudo systemctl stop nginx         # 停止服务
sudo systemctl restart nginx      # 重启服务
sudo systemctl enable nginx       # 设置开机自启
sudo systemctl disable nginx      # 取消开机自启
sudo systemctl status nginx        # 查看服务状态
systemctl list-units --type=service --all  # 列出所有服务
```

> 注：Gentoo使用OpenRC、Slackware使用rc.d脚本，但systemctl在Gentoo和Slackware中也可使用。

#### 2. 终端通用快捷键

```bash
Ctrl + C    # 终止当前正在执行的命令
Ctrl + L    # 清空屏幕（等同于clear命令）
Tab         # 自动补全命令/文件/目录名
Ctrl + Z    # 暂停当前命令，后续可通过fg恢复
Ctrl + D    # 退出当前终端会话
Ctrl + A    # 移动光标到行首
Ctrl + E    # 移动光标到行尾
Ctrl + U    # 删除光标前的所有字符
Ctrl + K    # 删除光标后的所有字符
```

#### 3. 权限说明

所有修改系统配置、安装/卸载软件、启停服务的命令，均需加sudo（管理员权限），避免权限不足报错。

```bash
# 示例
sudo apt install nginx        # 安装软件
sudo systemctl start nginx   # 启动服务
sudo rm -rf /tmp/test        # 删除目录
```

#### 4. 发行版识别命令

```bash
# 查看发行版信息
cat /etc/os-release

# 识别发行版类别
cat /etc/os-release | grep -E "^ID="

# 查看内核版本
uname -a

# 查看系统架构
arch
```

### 四、支持的发行版汇总

| 发行版系列 | 代表发行版 | 包管理器 | 服务管理器 | 防火墙 |
|-----------|-----------|---------|-----------|--------|
| Debian系 | Ubuntu, Debian, Linux Mint, Kali, Deepin | apt | systemd | ufw |
| RHEL系 | CentOS, RHEL, Fedora, Rocky, AlmaLinux | yum/dnf | systemd | firewalld |
| SUSE系 | openSUSE, SLES | zypper | systemd | firewalld |
| Arch系 | Arch Linux, Manjaro, Garuda | pacman | systemd | ufw |
| Gentoo系 | Gentoo, Funtoo | emerge | OpenRC | - |
| Slackware | Slackware | sbopkg/slackpkg | rc.d | - |

---

**操作系统智能代理** - 让系统管理更智能、更简单！
