Summary:	Mir display server and libraries
Summary(pl.UTF-8):	Serwer wyświetlania Mir oraz biblioteki
Name:		mir
Version:	0.1.8
Release:	0.1
License:	LGPL v3 (libraries), GPL v3 (server and examples)
Group:		Libraries
#Source0Download: https://launchpad.net/mir/+download
Source0:	https://launchpad.net/mir/trusty/%{version}/+download/%{name}-%{version}.tar.bz2
# Source0-md5:	bed92c675df5e670188a44307255bfa9
Patch0:		%{name}-c++.patch
Patch1:		%{name}-werror.patch
URL:		https://launchpad.net/mir
BuildRequires:	EGL-devel
BuildRequires:	GLM
BuildRequires:	Mesa-libgbm-devel >= 9.0.0
BuildRequires:	OpenGLESv2-devel
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	gmock-devel >= 1.7.0-2
BuildRequires:	gtest-devel >= 1.7.0-2
BuildRequires:	libdrm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	lttng-ust-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	python >= 2
BuildRequires:	udev-devel
BuildRequires:	umockdev-devel >= 0.6
BuildRequires:	xorg-lib-libxkbcommon-devel
# TODO? astyle pdebuild android-ndk android-sdk vera++
Requires:	Mesa-libgbm >= 9.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# __once_call, __once_called non-function symbols from libstdc++
%define		skip_post_check_so	libmirprotobuf.* libmirserver.*

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
Requires:	protobuf-devel

%description devel
Header files for Mir libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Mir.

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

%build
install -d build
cd build
%cmake .. \
	-DBUILD_DOXYGEN=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_{acceptance,integration,unit}_tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mir_stress

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/mir_demo_*
%attr(755,root,root) %{_bindir}/mirout
%attr(755,root,root) %{_bindir}/mirping
%attr(755,root,root) %{_bindir}/mirscreencast
%attr(755,root,root) %{_libdir}/libmirclient.so.7
%attr(755,root,root) %{_libdir}/libmirplatform.so
%attr(755,root,root) %{_libdir}/libmirprotobuf.so.0
%attr(755,root,root) %{_libdir}/libmirserver.so.18
%dir %{_libdir}/mir
%dir %{_libdir}/mir/clientplatform
%dir %{_libdir}/mir/clientplatform/mesa
%attr(755,root,root) %{_libdir}/mir/clientplatform/mesa/libmirclientplatform.so
%dir %{_libdir}/mir/platformgraphics
%dir %{_libdir}/mir/platformgraphics/mesa
%attr(755,root,root) %{_libdir}/mir/platformgraphics/mesa/libmirplatformgraphics.so
%dir %{_libdir}/mir/tools
%attr(755,root,root) %{_libdir}/mir/tools/libmirclientlttng.so
%attr(755,root,root) %{_libdir}/mir/tools/libmirserverlttng.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmirclient.so
%attr(755,root,root) %{_libdir}/libmirprotobuf.so
%attr(755,root,root) %{_libdir}/libmirserver.so
%{_includedir}/mirclient
%{_includedir}/mircommon
%{_includedir}/mirplatform
%{_includedir}/mirserver
%{_pkgconfigdir}/mirclient.pc
%{_pkgconfigdir}/mircommon.pc
%{_pkgconfigdir}/mirserver.pc
%dir %{_datadir}/mir
%{_datadir}/mir/protocol

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/mir-doc
