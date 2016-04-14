#
# Conditional build:
%bcond_with	android		# Android platform support (TODO)
#
Summary:	Mir display server and libraries
Summary(pl.UTF-8):	Serwer wyświetlania Mir oraz biblioteki
Name:		mir
Version:	0.21.0
Release:	0.1
License:	LGPL v3 (libraries), GPL v3 (server and examples)
Group:		Libraries
#Source0Download: https://launchpad.net/mir/+download
Source0:	https://launchpad.net/mir/0.21/%{version}/+download/%{name}-%{version}.tar.xz
# Source0-md5:	65e3e05420d59505f486b545b7c77ffc
Patch0:		%{name}-werror.patch
Patch1:		%{name}-gflags.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-libdrm.patch
Patch4:		%{name}-libinput.patch
URL:		https://launchpad.net/mir
BuildRequires:	EGL-devel
BuildRequires:	GLM
BuildRequires:	Mesa-libgbm-devel >= 9.0.0
BuildRequires:	OpenGLESv2-devel
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	gflags-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	glog-devel
BuildRequires:	gmock-devel >= 1.7.0-2
BuildRequires:	gtest-devel >= 1.7.0-2
BuildRequires:	libdrm-devel
# >1.2.x without libinput patch?
BuildRequires:	libinput-devel >= 1.2
# -std=c++14
BuildRequires:	libstdc++-devel >= 6:4.9
BuildRequires:	libuuid-devel
BuildRequires:	lttng-ust-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 2.4.1
BuildRequires:	python >= 2
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	umockdev-devel >= 0.6
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
# TODO? astyle pdebuild android-ndk android-sdk vera++
Requires:	Mesa-libgbm >= 9.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# __once_call, __once_called non-function symbols from libstdc++
%define		skip_post_check_so	libmirclient.so.* libmirclient-debug-extension.so.* libmirprotobuf.* libmirserver.*

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i -e 's/-Werror //' CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	-DBUILD_DOXYGEN=ON \
	-DMIR_PLATFORM="mesa-kms;mesa-x11;%{?with_android:;android}" \
	-DMIR_USE_PRECOMPILED_HEADERS=OFF
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_{acceptance,integration,performance,privileged,unit,umock_acceptance,umock_unit}_tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_{integration,unit}_tests_mesa*
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_stress
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_test_reload_protobuf
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mir-test-data

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/mir_demo_*
%attr(755,root,root) %{_bindir}/mir_proving_server
%attr(755,root,root) %{_bindir}/mirbacklight
%attr(755,root,root) %{_bindir}/mirin
%attr(755,root,root) %{_bindir}/mirout
%attr(755,root,root) %{_bindir}/mirping
%attr(756,root,root) %{_bindir}/mirscreencast
%attr(755,root,root) %{_libdir}/libmirclient.so.9
%attr(755,root,root) %{_libdir}/libmirclient-debug-extension.so.1
%attr(755,root,root) %{_libdir}/libmircommon.so.5
%attr(755,root,root) %{_libdir}/libmircookie.so.2
%attr(755,root,root) %{_libdir}/libmirplatform.so.11
%attr(755,root,root) %{_libdir}/libmirprotobuf.so.3
%attr(755,root,root) %{_libdir}/libmirserver.so.38
%attr(755,root,root) %{_libdir}/libmir_demo_server_loadable.so
%dir %{_libdir}/mir
%dir %{_libdir}/mir/client-platform
%attr(755,root,root) %{_libdir}/mir/client-platform/dummy.so
%attr(755,root,root) %{_libdir}/mir/client-platform/mesa.so.5
%dir %{_libdir}/mir/server-platform
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-dummy.so
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-mesa-kms.so.8
%attr(755,root,root) %{_libdir}/mir/server-platform/graphics-throw.so
%attr(755,root,root) %{_libdir}/mir/server-platform/input-evdev.so.5
%attr(755,root,root) %{_libdir}/mir/server-platform/input-stub.so
%attr(755,root,root) %{_libdir}/mir/server-platform/server-mesa-x11.so.8
%dir %{_libdir}/mir/tools
%attr(755,root,root) %{_libdir}/mir/tools/libmirclientlttng.so
%attr(755,root,root) %{_libdir}/mir/tools/libmirserverlttng.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmirclient.so
%attr(755,root,root) %{_libdir}/libmirclient-debug-extension.so
%attr(755,root,root) %{_libdir}/libmircommon.so
%attr(755,root,root) %{_libdir}/libmircookie.so
%attr(755,root,root) %{_libdir}/libmirplatform.so
%attr(755,root,root) %{_libdir}/libmirprotobuf.so
%attr(755,root,root) %{_libdir}/libmirserver.so
%{_includedir}/mirclient
%{_includedir}/mircommon
%{_includedir}/mircookie
%{_includedir}/mirplatform
%{_includedir}/mirrenderer
%{_includedir}/mirserver
%{_pkgconfigdir}/mir-client-platform-mesa.pc
%{_pkgconfigdir}/mir-renderer-gl-dev.pc
%{_pkgconfigdir}/mirclient.pc
%{_pkgconfigdir}/mirclient-debug-extension.pc
%{_pkgconfigdir}/mircookie.pc
%{_pkgconfigdir}/mirplatform.pc
%{_pkgconfigdir}/mirserver.pc

%files test-devel
%defattr(644,root,root,755)
%{_libdir}/libmir-test-assist.a
%{_includedir}/mirtest
%{_pkgconfigdir}/mirtest.pc
%{_datadir}/mir-perf-framework

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/mir-doc
