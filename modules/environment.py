import os
import platform
import subprocess

class EnvironmentDetector:
    def __init__(self):
        pass

    def get_environment_info(self):
        os_info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
        }

        if os_info['system'] == 'Linux':
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('NAME='):
                            os_info['distro'] = line.split('=')[1].strip('"')
                        elif line.startswith('VERSION='):
                            os_info['distro_version'] = line.split('=')[1].strip('"')
                        elif line.startswith('ID='):
                            os_info['distro_id'] = line.split('=')[1].strip('"')
            except FileNotFoundError:
                pass

            os_info['distro_category'] = self._detect_distro_category(os_info.get('distro_id', ''))
            os_info['package_manager'] = self.get_package_manager_info(os_info.get('distro_category', 'other'))
            os_info['service_manager'] = self.get_service_manager_info(os_info.get('distro_category', 'other'))

        os_info['user'] = os.getenv('USER') or os.getenv('USERNAME')
        os_info['hostname'] = platform.node()

        return os_info

    def _detect_distro_category(self, distro_id):
        debian_based = ['ubuntu', 'debian', 'linuxmint', 'pop', 'zorin', 'kali', 'parrot', 'deepin', 'uos']
        rhel_based = ['centos', 'rhel', 'fedora', 'rocky', 'alma', 'ol', 'amazon']
        suse_based = ['opensuse', 'sles', 'suse', 'suse-linux']
        arch_based = ['arch', 'manjaro', 'endeavouros', 'garuda', 'archlabs']
        gentoo_based = ['gentoo', 'funtoo']
        slackware_based = ['slackware']

        distro_lower = distro_id.lower()

        if distro_lower in debian_based:
            return 'debian'
        elif distro_lower in rhel_based:
            return 'rhel'
        elif distro_lower in suse_based:
            return 'suse'
        elif distro_lower in arch_based:
            return 'arch'
        elif distro_lower in gentoo_based:
            return 'gentoo'
        elif distro_lower in slackware_based:
            return 'slackware'
        else:
            return 'other'

    def get_package_manager(self):
        os_info = self.get_environment_info()
        if os_info['system'] != 'Linux':
            return None

        category = os_info.get('distro_category', 'other')

        package_managers = {
            'debian': 'apt',
            'rhel': 'yum/dnf',
            'suse': 'zypper',
            'arch': 'pacman',
            'gentoo': 'emerge',
            'slackware': 'sbopkg/slackpkg',
            'other': 'unknown'
        }

        return package_managers.get(category, 'unknown')

    def get_package_manager_info(self, category):
        package_manager_commands = {
            'debian': {
                'name': 'apt',
                'update': 'sudo apt update',
                'install': 'sudo apt install',
                'remove': 'sudo apt remove',
                'upgrade': 'sudo apt upgrade',
                'clean': 'sudo apt clean',
                'search': 'apt search',
                'local_install': 'sudo dpkg -i',
                'fix_deps': 'sudo apt -f install'
            },
            'rhel': {
                'name': 'yum/dnf',
                'update': 'sudo dnf check-update / sudo yum check-update',
                'install': 'sudo dnf install / sudo yum install',
                'remove': 'sudo dnf remove / sudo yum remove',
                'upgrade': 'sudo dnf upgrade / sudo yum update',
                'clean': 'sudo dnf clean all',
                'search': 'dnf search / yum search',
                'local_install': 'sudo rpm -ivh',
                'fix_deps': 'sudo dnf install -y'
            },
            'suse': {
                'name': 'zypper',
                'update': 'sudo zypper refresh',
                'install': 'sudo zypper install',
                'remove': 'sudo zypper remove',
                'upgrade': 'sudo zypper update',
                'clean': 'sudo zypper clean',
                'search': 'sudo zypper search',
                'local_install': 'sudo zypper install',
                'fix_deps': 'sudo zypper install -y'
            },
            'arch': {
                'name': 'pacman',
                'update': 'sudo pacman -Syu',
                'install': 'sudo pacman -S',
                'remove': 'sudo pacman -R',
                'upgrade': 'sudo pacman -Syu',
                'clean': 'sudo pacman -Sc / sudo pacman -Scc',
                'search': 'pacman -Ss',
                'local_install': 'sudo pacman -U',
                'fix_deps': 'sudo pacman -Syu'
            },
            'gentoo': {
                'name': 'emerge',
                'update': 'sudo emerge --sync',
                'install': 'sudo emerge',
                'remove': 'sudo emerge --deselect',
                'upgrade': 'sudo emerge -uDN @world',
                'clean': 'sudo eclean',
                'search': 'sudo emerge --search',
                'local_install': 'sudo emerge',
                'fix_deps': 'sudo emerge --depclean'
            },
            'slackware': {
                'name': 'sbopkg/slackpkg',
                'update': 'sudo slackpkg update',
                'install': 'sudo slackpkg install-package',
                'remove': 'sudo slackpkg remove-package',
                'upgrade': 'sudo slackpkg upgrade-all',
                'clean': 'sudo slackpkg clean-system',
                'search': 'sudo slackpkg search',
                'local_install': 'sudo installpkg',
                'fix_deps': 'sudo slackpkg install-new'
            },
            'other': {
                'name': 'unknown',
                'update': '',
                'install': '',
                'remove': '',
                'upgrade': '',
                'clean': '',
                'search': '',
                'local_install': '',
                'fix_deps': ''
            }
        }

        return package_manager_commands.get(category, package_manager_commands['other'])

    def get_service_manager(self):
        os_info = self.get_environment_info()
        if os_info['system'] != 'Linux':
            return None

        category = os_info.get('distro_category', 'other')

        if category in ['debian', 'rhel', 'suse', 'arch']:
            return 'systemd'
        elif category == 'gentoo':
            return 'OpenRC'
        elif category == 'slackware':
            return 'rc.d'
        else:
            return 'unknown'

    def get_service_manager_info(self, category):
        service_manager_commands = {
            'systemd': {
                'start': 'sudo systemctl start',
                'stop': 'sudo systemctl stop',
                'restart': 'sudo systemctl restart',
                'enable': 'sudo systemctl enable',
                'disable': 'sudo systemctl disable',
                'status': 'sudo systemctl status',
                'list': 'systemctl list-units --type=service --all'
            },
            'OpenRC': {
                'start': 'sudo rc-service start',
                'stop': 'sudo rc-service stop',
                'restart': 'sudo rc-service restart',
                'enable': 'sudo rc-update add',
                'disable': 'sudo rc-update del',
                'status': 'sudo rc-service status',
                'list': 'rc-update show'
            },
            'rc.d': {
                'start': 'sudo /etc/rc.d/rc.local start',
                'stop': 'sudo /etc/rc.d/rc.local stop',
                'restart': 'sudo /etc/rc.d/rc.local restart',
                'enable': 'chmod +x /etc/rc.d/rc.local',
                'disable': 'chmod -x /etc/rc.d/rc.local',
                'status': 'sudo /etc/rc.d/rc.local status',
                'list': 'ls /etc/rc.d/'
            },
            'unknown': {
                'start': '',
                'stop': '',
                'restart': '',
                'enable': '',
                'disable': '',
                'status': '',
                'list': ''
            }
        }

        return service_manager_commands.get(category, service_manager_commands['unknown'])

    def get_network_tools(self):
        os_info = self.get_environment_info()
        if os_info['system'] != 'Linux':
            return None

        category = os_info.get('distro_category', 'other')

        if category == 'debian':
            return {'ifconfig': 'net-tools', 'ip': 'iproute2', 'ss': 'iproute2', 'ping': 'iputils-ping', 'curl': 'curl', 'wget': 'wget'}
        elif category in ['rhel', 'suse']:
            return {'ifconfig': 'net-tools', 'ip': 'iproute2', 'ss': 'iproute2', 'ping': 'iputils', 'curl': 'curl', 'wget': 'wget'}
        elif category == 'arch':
            return {'ifconfig': 'net-tools', 'ip': 'iproute2', 'ss': 'iproute2', 'ping': 'iputils', 'curl': 'curl', 'wget': 'wget'}
        elif category == 'gentoo':
            return {'ifconfig': 'net-tools', 'ip': 'iproute2', 'ss': 'iproute2', 'ping': 'iputils', 'curl': 'curl', 'wget': 'wget'}
        else:
            return {'ifconfig': 'net-tools', 'ip': 'iproute2', 'ss': 'iproute2', 'ping': 'iputils', 'curl': 'curl', 'wget': 'wget'}

    def get_firewall_commands(self, category):
        firewall_commands = {
            'debian': {
                'ufw_status': 'sudo ufw status',
                'ufw_allow': 'sudo ufw allow',
                'ufw_deny': 'sudo ufw deny',
                'ufw_enable': 'sudo ufw enable',
                'ufw_disable': 'sudo ufw disable'
            },
            'rhel': {
                'firewalld_status': 'sudo firewall-cmd --state',
                'firewalld_list': 'sudo firewall-cmd --list-all',
                'firewalld_allow': 'sudo firewall-cmd --add-port',
                'firewalld_deny': 'sudo firewall-cmd --remove-port',
                'firewalld_reload': 'sudo firewall-cmd --reload'
            },
            'suse': {
                'firewalld_status': 'sudo firewall-cmd --state',
                'firewalld_list': 'sudo firewall-cmd --list-all',
                'firewalld_allow': 'sudo firewall-cmd --add-port',
                'firewalld_deny': 'sudo firewall-cmd --remove-port',
                'firewalld_reload': 'sudo firewall-cmd --reload'
            },
            'arch': {
                'ufw_status': 'sudo ufw status',
                'ufw_allow': 'sudo ufw allow',
                'ufw_deny': 'sudo ufw deny',
                'ufw_enable': 'sudo ufw enable',
                'ufw_disable': 'sudo ufw disable'
            },
            'other': {
                'ufw_status': '',
                'ufw_allow': '',
                'ufw_deny': '',
                'ufw_enable': '',
                'ufw_disable': ''
            }
        }

        return firewall_commands.get(category, firewall_commands['other'])
