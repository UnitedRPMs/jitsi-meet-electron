%global debug_package %{nil}
%define _build_id_links none
%undefine _missing_build_ids_terminate_build
AutoReqProv: no
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global nodjs_ver 14.18.2

%if 0%{?fedora} >= 35
%bcond_with  system_node
%define npm_ export PATH=%{_topdir}/node-v%{nodjs_ver}-linux-x64/bin/:$PATH && %{_topdir}/node-v%{nodjs_ver}-linux-x64/bin/npm
%else
%bcond_without  system_node
%global npm_ /usr/bin/npm
%endif

Name:		jitsi-meet-electron
Version:	2022.2.1
Release:	1%{?dist}
Summary:	Open Source Video Calls And Chat
Group:		Applications/Communications
License:	LGPLv2+
URL:		https://jitsi.org/
Source0:	https://github.com/jitsi/jitsi-meet-electron/archive/refs/tags/v%{version}.tar.gz
Source2:	jitsi-meet-electron.desktop
Source3:	org.jitsi-meet-electron.metainfo.xml
%if !%{with system_node}
Source4:	https://nodejs.org/dist/v%{nodjs_ver}/node-v%{nodjs_ver}-linux-x64.tar.xz
%endif

BuildRequires:	git wget make
BuildRequires:	libX11-devel
%if %{with system_node}
BuildRequires:	nodejs-devel npm
%else
BuildRequires:	electron
%endif
BuildRequires:	libpng-devel
BuildRequires:	gcc-c++ 
BuildRequires:	libXtst-devel
BuildRequires:	libxcrypt-compat
BuildRequires:	/usr/bin/python3



%description
Desktop application for Jitsi Meet built with Electron.


%prep
%if %{with system_node}
%setup -qn jitsi-meet-electron-%{version}
%else
%setup -n jitsi-meet-electron-%{version} -a4

mv -f node-v%{nodjs_ver}-linux-x64 %{_topdir}/
%endif

%build
rm package-lock.json
%npm_ config set registry https://registry.npmjs.org/ 
#npm  cache clean --force
%npm_ install node-gyp
%npm_  install nodejs-webpack
%npm_  install electron-builder
%npm_  install
#npm_  audit fix 
%npm_  run dist

%install
    mkdir -p -- %{buildroot}/%{_datadir}/applications
    cp -f %{S:2} %{buildroot}/%{_datadir}/applications/

    mkdir -p -- %{buildroot}/%{_datadir}
    cp -aT -- ./dist/linux-unpacked %{buildroot}/%{_datadir}/jitsi-meet-electron

    mkdir -p -- %{buildroot}/usr/bin
    ln -s -- '../share/jitsi-meet-electron/jitsi-meet' %{buildroot}/%{_bindir}/jitsi-meet-electron

    install -Dm644 -- resources/icon.png "%{buildroot}/%{_datadir}/pixmaps/%{name}.png"

# Appdata
install -Dm 0644 %{S:3} %{buildroot}/%{_metainfodir}/org.jitsi-meet-electron.metainfo.xml


%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/org.jitsi-meet-electron.metainfo.xml
%{_datadir}/pixmaps/%{name}*


%changelog

* Mon Mar 07 2022 David Va <davidva AT tuta DOT io> 2022.2.1-1
- Updated to 2022.2.1

* Wed Mar 02 2022 David Va <davidva AT tuta DOT io> 2022.1.1-1
- Updated to 2022.1.1

* Sun Dec 19 2021 Sérgio Basto <sergio@serjux.com> - 2021.12.2-1
- Update to 2021.12.2

* Sun Oct 10 2021 Sérgio Basto <sergio@serjux.com> - 2.9.0-1
- Update jitsi-meet-electron to 2.9.0

* Mon Aug 30 2021 David Va <davidva AT tuta DOT io> 2.8.11-1
- Updated to  2.8.11

* Sun Jul 04 2021 David Va <davidva AT tuta DOT io> 2.8.8-1
- Updated to  2.8.8

* Thu Jul 01 2021 David Va <davidva AT tuta DOT io> 2.8.7-1
- Updated to  2.8.7

* Fri Jun 04 2021 David Va <davidva AT tuta DOT io> 2.8.6-1
- Initial build
