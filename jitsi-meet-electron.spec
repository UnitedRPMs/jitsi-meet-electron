%global debug_package %{nil}
%define _build_id_links none
%undefine _missing_build_ids_terminate_build
AutoReqProv: no
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global nodjs_ver 14.18.0

%if 0%{?fedora} >= 34
%define npm_ export PATH=%{_topdir}/node-v%{nodjs_ver}-linux-x64/bin/:$PATH && %{_topdir}/node-v%{nodjs_ver}-linux-x64/bin/npm
%else 
%global npm_ /usr/bin/npm
%endif

Name:		jitsi-meet-electron
Version:	2.9.0
Release:	1%{?dist}
Summary:	Open Source Video Calls And Chat
Group:		Applications/Communications
License:	LGPLv2+
URL:		https://jitsi.org/
Source0:	https://github.com/jitsi/jitsi-meet-electron/archive/refs/tags/v%{version}.tar.gz
Source2:	jitsi-meet-electron.desktop
Source3:	org.jitsi-meet-electron.metainfo.xml
Source4:	https://nodejs.org/dist/v14.18.0/node-v%nodjs_ver-linux-x64.tar.xz

BuildRequires:	git wget make
BuildRequires:	libX11-devel
BuildRequires:	electron
%if 0%{?fedora} <= 33
BuildRequires:	nodejs-devel npm
%endif
BuildRequires:	libpng-devel
BuildRequires:	gcc-c++ 
BuildRequires:	libXtst-devel
BuildRequires:	libxcrypt-compat
BuildRequires:	/usr/bin/python3



%description
Desktop application for Jitsi Meet built with Electron.


%prep
%setup -n jitsi-meet-electron-%{version} -a4

%if 0%{?fedora} >= 34
mv -f node-v%{nodjs_ver}-linux-x64 %{_topdir}/
%endif

%build
%npm_ config set registry https://registry.npmjs.org/ 
%npm_ cache clean --force
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
    ln -s -- '../share/jitsi-meet-electron/jitsi-meet.bin' %{buildroot}/%{_bindir}/jitsi-meet-electron

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
