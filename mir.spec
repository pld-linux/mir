Summary:	Mir display server and libraries
Summary(pl.UTF-8):	Serwer wyświetlania Mir oraz biblioteki
Name:		mir
Version:	1.8.2
Release:	0.1
License:	LGPL v3 (libraries), GPL v3 (server and examples)
Group:		Libraries
#Source0Download: https://github.com/MirServer/mir/releases
Source0:	https://github.com/MirServer/mir/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	d662d1ea8c1f0b34ddd95eb9c6a8a26b
Patch1:		%{name}-gflags.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-atomic.patch
Patch4:		%{name}-c++.patch
Patch5:		%{name}-gtest.patch
Patch6:		%{name}-wayland.patch
Patch7:		%{name}-capnproto.patch
URL:		https://mir-server.io/
BuildRequires:	EGL-devel
BuildRequires:	GLM
BuildRequires:	Mesa-libgbm-devel >= 11.0
BuildRequires:	OpenGLESv2-devel
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	capnproto-c++-devel
BuildRequires:	cmake >= 3.5
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	egl-wayland-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	gflags-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	glog-devel
BuildRequires:	gmock-devel >= 1.7.0-2
BuildRequires:	gtest-devel >= 1.7.0-2
BuildRequires:	libdrm-devel >= 2.4.84
BuildRequires:	libepoxy-devel
BuildRequires:	libevdev-devel
BuildRequires:	libinput-devel >= 1.2
# -std=c++14
BuildRequires:	libstdc++-devel >= 6:4.9
BuildRequires:	libuuid-devel
# xcb xcb-composite xcb-fixes xcb-render
BuildRequires:	libxcb-devel
BuildRequires:	libxml++2-devel >= 2.6
BuildRequires:	lttng-ust-devel
BuildRequires:	nettle-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 2.4.1
BuildRequires:	python >= 3
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	umockdev-devel >= 0.6
# wayland-client, wayland-server
BuildRequires:	wayland-devel
BuildRequires:	wayland-egl-devel
BuildRequires:	wlcs-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
BuildRequires:	yaml-cpp-devel
Requires:	Mesa-libgbm >= 11.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# __once_call, __once_called non-function symbols from libstdc++
%define		skip_post_check_so	libmirclient.so.* libmirprotobuf.* libmirserver.*

%description
Mir is a next generation display server targeted as a replacement for
the X Window server system to unlock next-generation user experiences
for devices ranging from Linux desktop to mobile devices powered by
Ubuntu. The primary purpose of Mir is to enable the development of the
next generation Unity (<http://unity.ubuntu.com/>).

%description -l pl.UTF-8
Mir to serwer wyświetlania nowej generacji, tworzony jako zamiennik
systemu serwera X Window, aby pozwolić użytkownikom na doznania nowej
generacji na urządzeniach od biurkowego komputera z Linuksem do
urządzeń przenośnych z działającym Ubuntu. Głównym celem Mira jest
umożliwienie rozwoju interfejsu Unity nowej generacji
(<http://unity.ubuntu.com/>).

%package devel
Summary:	Header files for Mir libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Mir
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	protobuf-devel >= 2.4.1

%description devel
Header files for Mir libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Mir.

%package test-devel
Summary:	Development package for Mir tests
Summary(pl.UTF-8):	Pakiet programistyczny dla testów Mira
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description test-devel
Development package for Mir tests.

%description test-devel -l pl.UTF-8
Pakiet programistyczny dla testów Mira.

%package apidocs
Summary:	Mir API documentation
Summary(pl.UTF-8):	Dokumentacja API Mira
Group:		Documentation

%description apidocs
API documentation for Mir.

%description apidocs -l pl.UTF-8
Dokumentacja API Mira.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{__sed} -i -e 's/-Werror //' CMakeLists.txt

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' \
	examples/miral-shell/miral-app.sh \
	examples/miral-shell/desktop/mir-shell.sh

%build
install -d build
cd build
# override unsuccessful "detection" by "rpm -q libgtest-dev"
export GTEST_VERSION="$(gtest-config --version)"
%cmake .. \
	-DBUILD_DOXYGEN=ON \
	-DMIR_PLATFORM="mesa-kms;mesa-x11;eglstream-kms" \
	-DMIR_USE_PRECOMPILED_HEADERS=OFF
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir-smoke-test-runner
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_performance_tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_platform_graphics_test_harness
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_stress

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/mir-shell
%attr(755,root,root) %{_bindir}/mir_demo_*
%attr(755,root,root) %{_bindir}/miral-app
%attr(755,root,root) %{_bindir}/miral-kiosk
%attr(755,root,root) %{_bindir}/miral-shell
%attr(755,root,root) %{_bindir}/miral-system-compositor
%attr(755,root,root) %{_bindir}/miral-terminal
%attr(755,root,root) %{_bindir}/mirin
%attr(755,root,root) %{_bindir}/mirout
%attr(756,root,root) %{_bindir}/mirscreencast
%attr(755,root,root) %{_libdir}/libmiral.so.3
%attr(755,root,root) %{_libdir}/libmirclient.so.9
%attr(755,root,root) %{_libdir}/libmircommon.so.7
%attr(755,root,root) %{_libdir}/libmircookie.so.2
%attr(755,root,root) %{_libdir}/libmircore.so.1
%attr(755,root,root) %{_libdir}/libmirplatform.so.18
%attr(755,root,root) %{_libdir}/libmirprotobuf.so.3
%attr(755,root,root) %{_libdir}/libmirserver.so.53
%attr(755,root,root) %{_libdir}/libmirwayland.so.0
%dir %{_libdir}/mir
%attr(755,root,root) %{_libdir}/mir/miral_wlcs_integration.so
%dir %{_libdir}/mir/client-platform
%attr(755,root,root) %{_libdir}/mir/client-platform/dummy.so
%attr(755,root,root) %{_libdir}/mir/client-platform/mesa.so.5
%dir %{_libdir}/mir/server-platform
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-dummy.so
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-eglstream-kms.so.16
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-mesa-kms.so.16
%attr(755,root,root) %{_libdir}/mir/server-platform/input-evdev.so.7
%attr(755,root,root) %{_libdir}/mir/server-platform/input-stub.so
%attr(755,root,root) %{_libdir}/mir/server-platform/server-mesa-x11.so.16
%dir %{_libdir}/mir/tools
%attr(755,root,root) %{_libdir}/mir/tools/libmirclientlttng.so
%attr(755,root,root) %{_libdir}/mir/tools/libmirserverlttng.so
%{_datadir}/wayland-sessions/mir-shell.desktop
%{_desktopdir}/miral-shell.desktop
%{_iconsdir}/hicolor/scalable/apps/ubuntu-logo.svg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mir_wayland_generator
%attr(755,root,root) %{_libdir}/libmiral.so
%attr(755,root,root) %{_libdir}/libmirclient.so
%attr(755,root,root) %{_libdir}/libmircommon.so
%attr(755,root,root) %{_libdir}/libmircookie.so
%attr(755,root,root) %{_libdir}/libmircore.so
%attr(755,root,root) %{_libdir}/libmirplatform.so
%attr(755,root,root) %{_libdir}/libmirprotobuf.so
%attr(755,root,root) %{_libdir}/libmirserver.so
%attr(755,root,root) %{_libdir}/libmirwayland.so
%{_includedir}/miral
%{_includedir}/mirclient
%{_includedir}/mircommon
%{_includedir}/mircookie
%{_includedir}/mircore
%{_includedir}/mirplatform
%{_includedir}/mirplatforms
%{_includedir}/mirrenderer
%{_includedir}/mirserver
%{_includedir}/mirwayland
%{_pkgconfigdir}/mir-client-platform-mesa.pc
%{_pkgconfigdir}/mir-renderer-gl-dev.pc
%{_pkgconfigdir}/miral.pc
%{_pkgconfigdir}/mirclient.pc
%{_pkgconfigdir}/mirclientcpp.pc
%{_pkgconfigdir}/mircommon.pc
%{_pkgconfigdir}/mircookie.pc
%{_pkgconfigdir}/mircore.pc
%{_pkgconfigdir}/mirplatform.pc
%{_pkgconfigdir}/mirrenderer.pc
%{_pkgconfigdir}/mirserver.pc
%{_pkgconfigdir}/mirwayland.pc

%files test-devel
%defattr(644,root,root,755)
%{_libdir}/libmir-test-assist.a
%{_includedir}/mirtest
%{py3_sitescriptdir}/mir_perf_framework
%{py3_sitescriptdir}/mir_perf_framework-%{version}-py*.egg-info
%{_pkgconfigdir}/mirtest.pc
%{_datadir}/mir-perf-framework

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/mir-doc
