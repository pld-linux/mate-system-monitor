Summary:	Process and resource monitor for MATE desktop
Summary(pl.UTF-8):	Monitor procesów w zasobów dla środowiska MATE
Name:		mate-system-monitor
Version:	1.18.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.18/%{name}-%{version}.tar.xz
# Source0-md5:	16cd6a8ffb4212f735ca9b229ce20324
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	glibmm-devel >= 2.26.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	gtkmm3-devel >= 3.8.1
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libgtop-devel >= 1:2.23.1
BuildRequires:	librsvg-devel >= 2.35
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libwnck-devel >= 3.0.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-common
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	startup-notification-devel
BuildRequires:	systemd-devel >= 44
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	glib2 >= 1:2.36.0
Requires:	glibmm >= 2.26.0
Requires:	gtk+3 >= 3.14.0
Requires:	gtkmm3 >= 3.8.1
Requires:	libgtop >= 1:2.23.1
Requires:	librsvg >= 2.35
Requires:	libwnck >= 3.0.0
Requires:	mate-desktop
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mate-system-monitor allows to graphically view and manipulate the
running processes on your system. It also provides an overview of
available resources such as CPU and memory.

%description -l pl.UTF-8
mate-system-monitor pozwala na graficzny podgląd i operowanie na
procesach działających w systemie. Zapewnia także widok dostępnych
zasobów, takich jak procesor i pamięć.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-compile-warnings=minimum

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not supported by glibc (as of 2.24-1)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ku_IQ,jv,nah,pms}

desktop-file-install \
	--delete-original \
	--remove-category=MATE \
	--add-category=X-Mate \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%find_lang %{name} --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/mate-system-monitor.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}
%{_datadir}/appdata/mate-system-monitor.appdata.xml
%{_datadir}/glib-2.0/schemas/org.mate.system-monitor.*.xml
%{_datadir}/polkit-1/actions/org.mate.mate-system-monitor.policy
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/msm-kill
%attr(755,root,root) %{_libdir}/%{name}/msm-renice
