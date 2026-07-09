# The release tarball does not contain the data folder
%global commit d6ec36aae87e765eddef8308f0f58c7b5be95ad7
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           v4l2-relayd
Summary:        Streaming relay for v4l2loopback using GStreamer
Version:        0.2.0
Release:        3%{?dist}
License:        GPL-2.0-only
URL:            https://gitlab.com/vicamo/v4l2-relayd

Source0:        %{url}//-/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        v4l2-relayd.preset
Source2:        icamera.conf

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.36
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gstreamer-app-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gstreamer-video-1.0) >= 1.0.0
#BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

Requires:       v4l2loopback-kmod-common

%description
A daemon to stream the content from GStreamer video source into the v4l2loopback
device so the user can see its content in the virtual camera on the system.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
autoreconf -vif
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-systemdsystemgeneratordir=%{_systemdgeneratordir} \
    --with-modulesloaddir=%{_modulesloaddir}

%make_build

%install
# Why isn't this a configure parameter?....
%make_install modprobedir=%{_modprobedir}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_presetdir}/95-v4l2-relayd.preset
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/v4l2-relayd.d/icamera.conf

%post
%systemd_post v4l2-relayd.service

%preun
%systemd_preun v4l2-relayd.service

%postun
%systemd_postun_with_restart v4l2-relayd.service

%files
%license LICENSE
%doc README.md
%{_bindir}/v4l2-relayd
%{_sysconfdir}/default/v4l2-relayd
%dir %{_sysconfdir}/v4l2-relayd.d
%config %{_sysconfdir}/v4l2-relayd.d/icamera.conf
%{_modprobedir}/v4l2-relayd.conf
%{_modulesloaddir}/v4l2-relayd.conf
%{_systemdgeneratordir}/v4l2-relayd-generator
%{_unitdir}/v4l2-relayd.service
%{_unitdir}/v4l2-relayd@.service
%{_presetdir}/95-v4l2-relayd.preset

%changelog
* Thu Jul 09 2026 Simone Caronni <negativo17@gmail.com> - 0.2.0-3
- Update configuration for gstreamer icamerasrc.

* Tue Jul 07 2026 Simone Caronni <negativo17@gmail.com> - 0.2.0-2
- Adjust dependencies.

* Tue Jul 07 2026 Simone Caronni <negativo17@gmail.com> - 0.2.0-1
- First build.
