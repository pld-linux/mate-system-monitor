#
# Conditional build:
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x

Summary:	Process and resource monitor for MATE desktop
Summary(pl.UTF-8):	Monitor procesów w zasobów dla środowiska MATE
Name:		mate-system-monitor
Version:	1.8.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	d6b10ecda2d1d5f294bb54626d72f321
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	glibmm-devel >= 2.26.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.20.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
%{!?with_gtk3:BuildRequires:	gtkmm-devel >= 2.22}
%{?with_gtk3:BuildRequires:	gtkmm3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgtop-devel >= 1:2.23.1
BuildRequires:	librsvg-devel >= 2.12
BuildRequires:	libtool >= 1:1.4.3
%{?with_gtk3:BuildRequires:	libwnck-devel >= 3.0.0}
%{!?with_gtk3:BuildRequires:	libwnck2-devel >= 2.5.0}
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-common
BuildRequires:	mate-icon-theme-devel >= 1.1.0
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	startup-notification-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	glib2 >= 1:2.28.0
Requires:	glibmm >= 2.26.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.20.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
%{!?with_gtk3:Requires:	gtkmm >= 2.22}
%{?with_gtk3:Requires:	gtkmm3 >= 3.0.0}
Requires:	libgtop >= 1:2.23.1
Requires:	librsvg >= 2.12
%{?with_gtk3:Requires:	libwnck >= 3.0.0}
%{!?with_gtk3:Requires:	libwnck2 >= 2.5.0}
Requires:	mate-desktop
Requires:	mate-icon-theme >= 1.1.0
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
	--enable-compile-warnings=minimum \
	%{?with_gtk3:--with-gtk=3.0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/%{name}.convert

# not supported by glibc (as of 2.19-3)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/nah

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
%{_datadir}/glib-2.0/schemas/org.mate.system-monitor.*.xml
