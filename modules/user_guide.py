class UserGuide:
    def __init__(self):
        pass
    
    def get_initial_guide(self, distro_category, distro_name=None, version=None):
        """获取针对不同Linux发行版的初始操作指引"""
        guides = {
            'debian': self._get_debian_guide(distro_name, version),
            'rhel': self._get_rhel_guide(distro_name, version),
            'suse': self._get_suse_guide(distro_name, version),
            'arch': self._get_arch_guide(distro_name, version),
            'other': self._get_generic_guide(distro_name, version)
        }
        
        return guides.get(distro_category, guides['other'])
    
    def _get_debian_guide(self, distro_name, version):
        distro = distro_name or 'Debian/Ubuntu'
        return f"""
# {distro} 系统初始设置指南

## 1. 系统更新
```bash
sudo apt update && sudo apt upgrade -y
```

## 2. 安装常用工具
```bash
sudo apt install -y vim htop curl wget git
```

## 3. 网络配置
- 查看网络状态: `ip addr show`
- 测试网络连接: `ping -c 3 google.com`

## 4. 用户管理
- 创建新用户: `sudo adduser username`
- 添加到sudo组: `sudo usermod -aG sudo username`

## 5. 防火墙设置
```bash
sudo ufw status
sudo ufw enable
sudo ufw allow ssh
```

## 6. 系统监控
- 查看系统负载: `top`
- 查看磁盘使用: `df -h`
- 查看内存使用: `free -h`

## 7. 服务管理
- 查看服务状态: `systemctl status`
- 启动服务: `sudo systemctl start service_name`
- 启用服务: `sudo systemctl enable service_name`

## 8. 软件安装
- 安装软件: `sudo apt install package_name`
- 搜索软件: `apt search package_name`
- 移除软件: `sudo apt remove package_name`

## 9. 系统信息
- 查看系统版本: `lsb_release -a`
- 查看内核版本: `uname -r`
- 查看硬件信息: `lshw -short`

## 10. 常见问题
- 忘记密码: 进入单用户模式重置
- 网络问题: 检查 `/etc/netplan/` 配置
- 权限问题: 使用 `chmod` 和 `chown` 调整权限
"""
    
    def _get_rhel_guide(self, distro_name, version):
        distro = distro_name or 'CentOS/RHEL'
        return f"""
# {distro} 系统初始设置指南

## 1. 系统更新
```bash
sudo yum update -y  # 旧版本
sudo dnf update -y  # 新版本
```

## 2. 安装常用工具
```bash
sudo yum install -y vim htop curl wget git  # 旧版本
sudo dnf install -y vim htop curl wget git  # 新版本
```

## 3. 网络配置
- 查看网络状态: `ip addr show`
- 测试网络连接: `ping -c 3 google.com`
- 配置网络: `sudo nmcli connection modify eth0`

## 4. 用户管理
- 创建新用户: `sudo useradd -m username`
- 设置密码: `sudo passwd username`
- 添加到wheel组: `sudo usermod -aG wheel username`

## 5. 防火墙设置
```bash
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
```

## 6. 系统监控
- 查看系统负载: `top`
- 查看磁盘使用: `df -h`
- 查看内存使用: `free -h`

## 7. 服务管理
- 查看服务状态: `systemctl status`
- 启动服务: `sudo systemctl start service_name`
- 启用服务: `sudo systemctl enable service_name`

## 8. 软件安装
- 安装软件: `sudo yum install package_name` 或 `sudo dnf install package_name`
- 搜索软件: `yum search package_name` 或 `dnf search package_name`
- 移除软件: `sudo yum remove package_name` 或 `sudo dnf remove package_name`

## 9. 系统信息
- 查看系统版本: `cat /etc/redhat-release`
- 查看内核版本: `uname -r`
- 查看硬件信息: `lshw -short`

## 10. 常见问题
- 忘记密码: 进入救援模式重置
- 网络问题: 检查 `/etc/sysconfig/network-scripts/` 配置
- 权限问题: 使用 `chmod` 和 `chown` 调整权限
"""
    
    def _get_suse_guide(self, distro_name, version):
        distro = distro_name or 'openSUSE'
        return f"""
# {distro} 系统初始设置指南

## 1. 系统更新
```bash
sudo zypper refresh
sudo zypper update -y
```

## 2. 安装常用工具
```bash
sudo zypper install -y vim htop curl wget git
```

## 3. 网络配置
- 查看网络状态: `ip addr show`
- 测试网络连接: `ping -c 3 google.com`
- 配置网络: `sudo yast lan`

## 4. 用户管理
- 创建新用户: `sudo useradd -m username`
- 设置密码: `sudo passwd username`
- 添加到wheel组: `sudo usermod -aG wheel username`

## 5. 防火墙设置
```bash
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
```

## 6. 系统监控
- 查看系统负载: `top`
- 查看磁盘使用: `df -h`
- 查看内存使用: `free -h`

## 7. 服务管理
- 查看服务状态: `systemctl status`
- 启动服务: `sudo systemctl start service_name`
- 启用服务: `sudo systemctl enable service_name`

## 8. 软件安装
- 安装软件: `sudo zypper install package_name`
- 搜索软件: `zypper search package_name`
- 移除软件: `sudo zypper remove package_name`

## 9. 系统信息
- 查看系统版本: `cat /etc/os-release`
- 查看内核版本: `uname -r`
- 查看硬件信息: `lshw -short`

## 10. 常见问题
- 忘记密码: 进入救援模式重置
- 网络问题: 检查 `/etc/sysconfig/network/` 配置
- 权限问题: 使用 `chmod` 和 `chown` 调整权限
"""
    
    def _get_arch_guide(self, distro_name, version):
        distro = distro_name or 'Arch Linux'
        return f"""
# {distro} 系统初始设置指南

## 1. 系统更新
```bash
sudo pacman -Syu
```

## 2. 安装常用工具
```bash
sudo pacman -S vim htop curl wget git
```

## 3. 网络配置
- 查看网络状态: `ip addr show`
- 测试网络连接: `ping -c 3 google.com`
- 配置网络: `sudo nano /etc/systemd/network/20-ethernet.network`

## 4. 用户管理
- 创建新用户: `sudo useradd -m -G wheel username`
- 设置密码: `sudo passwd username`
- 配置sudo: `sudo EDITOR=nano visudo` (取消注释wheel组)

## 5. 防火墙设置
```bash
sudo pacman -S ufw
sudo ufw enable
sudo ufw allow ssh
```

## 6. 系统监控
- 查看系统负载: `top`
- 查看磁盘使用: `df -h`
- 查看内存使用: `free -h`

## 7. 服务管理
- 查看服务状态: `systemctl status`
- 启动服务: `sudo systemctl start service_name`
- 启用服务: `sudo systemctl enable service_name`

## 8. 软件安装
- 安装软件: `sudo pacman -S package_name`
- 搜索软件: `pacman -Ss package_name`
- 移除软件: `sudo pacman -R package_name`

## 9. 系统信息
- 查看系统版本: `cat /etc/os-release`
- 查看内核版本: `uname -r`
- 查看硬件信息: `lshw -short`

## 10. 常见问题
- 忘记密码: 进入单用户模式重置
- 网络问题: 检查网络配置文件
- 权限问题: 使用 `chmod` 和 `chown` 调整权限
"""
    
    def _get_generic_guide(self, distro_name, version):
        distro = distro_name or 'Linux'
        return f"""
# {distro} 系统初始设置指南

## 1. 系统更新
- Debian/Ubuntu: `sudo apt update && sudo apt upgrade -y`
- CentOS/RHEL: `sudo yum update -y` 或 `sudo dnf update -y`
- openSUSE: `sudo zypper refresh && sudo zypper update -y`
- Arch Linux: `sudo pacman -Syu`

## 2. 安装常用工具
- Debian/Ubuntu: `sudo apt install -y vim htop curl wget git`
- CentOS/RHEL: `sudo yum install -y vim htop curl wget git`
- openSUSE: `sudo zypper install -y vim htop curl wget git`
- Arch Linux: `sudo pacman -S vim htop curl wget git`

## 3. 网络配置
- 查看网络状态: `ip addr show`
- 测试网络连接: `ping -c 3 google.com`

## 4. 用户管理
- 创建新用户: `sudo useradd -m username` 或 `sudo adduser username`
- 设置密码: `sudo passwd username`
- 添加到管理员组: `sudo usermod -aG sudo username` 或 `sudo usermod -aG wheel username`

## 5. 防火墙设置
- Debian/Ubuntu: `sudo ufw enable && sudo ufw allow ssh`
- CentOS/RHEL: `sudo systemctl start firewalld && sudo firewall-cmd --add-service=ssh --permanent && sudo firewall-cmd --reload`

## 6. 系统监控
- 查看系统负载: `top`
- 查看磁盘使用: `df -h`
- 查看内存使用: `free -h`

## 7. 服务管理
- 查看服务状态: `systemctl status`
- 启动服务: `sudo systemctl start service_name`
- 启用服务: `sudo systemctl enable service_name`

## 8. 系统信息
- 查看系统版本: `cat /etc/os-release`
- 查看内核版本: `uname -r`
- 查看硬件信息: `lshw -short`

## 9. 常见问题
- 忘记密码: 进入单用户模式或救援模式重置
- 网络问题: 检查网络配置文件
- 权限问题: 使用 `chmod` 和 `chown` 调整权限
"""
    
    def get_specific_guide(self, topic, distro_category):
        """获取特定主题的操作指引"""
        guides = {
            'network': self._get_network_guide(distro_category),
            'security': self._get_security_guide(distro_category),
            'performance': self._get_performance_guide(distro_category),
            'storage': self._get_storage_guide(distro_category),
            'backup': self._get_backup_guide(distro_category)
        }
        
        return guides.get(topic, f"暂未提供关于 '{topic}' 的具体指引")
    
    def _get_network_guide(self, distro_category):
        guides = {
            'debian': "# Debian/Ubuntu 网络配置指南\n\n1. 查看网络接口: `ip addr show`\n2. 配置网络: `sudo nano /etc/netplan/00-installer-config.yaml`\n3. 应用配置: `sudo netplan apply`\n4. 重启网络: `sudo systemctl restart NetworkManager`",
            'rhel': "# CentOS/RHEL 网络配置指南\n\n1. 查看网络接口: `ip addr show`\n2. 配置网络: `sudo nano /etc/sysconfig/network-scripts/ifcfg-eth0`\n3. 重启网络: `sudo systemctl restart network`\n4. 使用nmcli: `sudo nmcli connection modify eth0`",
            'suse': "# openSUSE 网络配置指南\n\n1. 查看网络接口: `ip addr show`\n2. 配置网络: `sudo yast lan`\n3. 重启网络: `sudo systemctl restart NetworkManager`",
            'arch': "# Arch Linux 网络配置指南\n\n1. 查看网络接口: `ip addr show`\n2. 配置网络: `sudo nano /etc/systemd/network/20-ethernet.network`\n3. 重启网络: `sudo systemctl restart systemd-networkd`",
            'other': "# 通用网络配置指南\n\n1. 查看网络接口: `ip addr show`\n2. 测试网络: `ping -c 3 google.com`\n3. 查看路由: `ip route show`\n4. 检查DNS: `cat /etc/resolv.conf`"
        }
        return guides.get(distro_category, guides['other'])
    
    def _get_security_guide(self, distro_category):
        return "# 系统安全加固指南\n\n1. 更新系统: 定期运行系统更新命令\n2. 防火墙: 启用并配置防火墙\n3. SSH配置: 修改默认端口，禁用root登录\n4. 密码策略: 设置强密码策略\n5. 审计: 定期检查系统日志\n6. 软件: 只安装必要的软件包\n7. 权限: 最小权限原则\n8. 备份: 定期备份重要数据"
    
    def _get_performance_guide(self, distro_category):
        return "# 系统性能优化指南\n\n1. 监控资源: 使用htop、vmstat等工具\n2. 磁盘优化: 使用SSD，合理分区\n3. 内存管理: 调整swap设置\n4. 网络优化: 调整网络参数\n5. 服务管理: 禁用不必要的服务\n6. 内核参数: 根据硬件调整内核参数\n7. 文件系统: 使用合适的文件系统\n8. 定期维护: 清理临时文件，更新系统"
    
    def _get_storage_guide(self, distro_category):
        return "# 存储管理指南\n\n1. 查看磁盘: `lsblk`\n2. 分区: `fdisk` 或 `parted`\n3. 格式化: `mkfs.ext4` 或其他文件系统\n4. 挂载: 编辑 `/etc/fstab`\n5. LVM: 逻辑卷管理\n6. RAID: 磁盘阵列配置\n7. 空间管理: 定期清理，监控使用情况\n8. 备份: 定期备份重要数据"
    
    def _get_backup_guide(self, distro_category):
        return "# 系统备份指南\n\n1. 备份工具: rsync, tar, borgbackup等\n2. 备份策略: 完整备份 + 增量备份\n3. 备份位置: 外部存储，云端存储\n4. 自动化: 使用cron定期执行\n5. 验证: 定期测试备份恢复\n6. 重要数据: /etc, /home, 数据库等\n7. 灾难恢复: 准备恢复计划\n8. 安全: 加密备份数据"
