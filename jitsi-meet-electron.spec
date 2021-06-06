%global debug_package %{nil}
%define _build_id_links none
%undefine _missing_build_ids_terminate_build
AutoReqProv: no
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:		jitsi-meet-electron
Version:	2.8.6
Release:	1%{dist}
Summary:	Open Source Video Calls And Chat
Group:		Applications/Communications
License:	LGPLv2+
URL:		https://jitsi.org/
Source0:	https://github.com/jitsi/jitsi-meet-electron/archive/refs/tags/v%{version}.tar.gz
Source2:	jitsi-meet-electron.desktop
Source3:	org.jitsi.jitsi.metainfo.xml

BuildRequires:	git wget npm make
BuildRequires:	libX11-devel
BuildRequires:	electron
BuildRequires:	nodejs-devel 
BuildRequires:	libpng-devel
BuildRequires:	gcc-c++ 
BuildRequires:	libXtst-devel
BuildRequires:	libxcrypt-compat
Provides:	jitsi >= 2.11.5633


%description
Desktop application for Jitsi Meet built with Electron.


%prep
%setup -n jitsi-meet-electron-%{version} 

%build
npm config set registry http://registry.npmjs.org/ 
npm install node-gyp
npm install nodejs-webpack
npm install electron-builder
npm install
npm audit fix
npm run dist

%install
    mkdir -p -- %{buildroot}/%{_datadir}/applications
    cp -f %{S:2} %{buildroot}/%{_datadir}/applications/

    mkdir -p -- %{buildroot}/%{_datadir}
    cp -aT -- ./dist/linux-unpacked %{buildroot}/%{_datadir}/jitsi-meet-electron

    mkdir -p -- %{buildroot}/usr/bin
    ln -s -- '../share/jitsi-meet-electron/jitsi-meet.bin' %{buildroot}/%{_bindir}/jitsi-meet-electron

    install -Dm644 -- resources/icon.png "%{buildroot}/%{_datadir}/pixmaps/%{name}.png"

# Appdata
install -Dm 0644 %{S:3} %{buildroot}/%{_metainfodir}/org.jitsi.jitsi.metainfo.xml


%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/org.jitsi.jitsi.metainfo.xml
%{_datadir}/pixmaps/%{name}*


%changelog

* Fri Jun 04 2021 David Va <davidva AT tuta DOT io> 2.8.6-1
- Initial build
