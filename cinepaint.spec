#
# TODO:
#      - Correct building with --with print
#
# Conditional build:
%bcond_with	print	# build with libgutenprintui
%bcond_with	gtk1	# GTK+ 1.x instead of 2.x

Summary:	CinePaint - a motion picture editing tool
Summary(pl.UTF-8):	CinePaint - narzędzie do obróbki filmów
Name:		cinepaint
Version:	1.3
Release:	0.1
License:	GPL v2+ (with LGPL v2.1+ and MIT parts)
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/cinepaint/%{name}-%{version}.tgz
# Source0-md5:	f8ecd5671662e71a3356213de371fee4
Patch0:		%{name}-am.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-libpng.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-paths.patch
URL:		http://www.cinepaint.org/
BuildRequires:	OpenEXR-devel >= 1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	lcms-devel >= 1.16
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0.0
BuildRequires:	libtiff-devel
BuildRequires:	libtool
#BuildRequires:	oyranos-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
%{?with_print:BuildRequires:     libgutenprintui-devel >= 5.0.0}
%if %{with gtk1}
BuildRequires:	glib-devel
BuildRequires:	gtk+-devel >= 1.2.8
%else
BuildRequires:	gtk+2-devel >= 2.0.0
%endif
# FreeSans.ttf
Requires:	fonts-TTF-freefont
Obsoletes:	filmgimp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver	1.3.0

%description
CinePaint is a motion picture editing tool primarily used for painting
and retouching of movies. CinePaint is the most successful open source
tool in future motion picture work today. It was formerly known as
FilmGimp.

%description -l pl.UTF-8
CinePaint jest narzędziem do obróbki ruchomego obrazu, używanym
głównie do rysowania i retuszu filmów. Na dzień dzisiejszy jest
narzędziem z otwartymi źródłami, które odniosło największy sukces w
branży filmowej. Wcześniej było znane pod nazwą FilmGimp.

%package devel
Summary:	Header files for CinePaint libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek CinePainta
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	filmgimp-devel

%description devel
Header files for CinePaint libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek CinePainta.

%package static
Summary:	Static CinePaint libraries
Summary(pl.UTF-8):	Statyczne biblioteki CinePaint
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	filmgimp-static

%description static
Static CinePaint libraries.

%description static -l pl.UTF-8
Statyczne biblioteki CinePainta.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# dead symlinks
%{__rm} config.guess config.sub py-compile

%build
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__automake}
%configure \
	%{!?with_print:--disable-print}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gimpmodule.{la,a}
# provided by fonts-TTF-freefont
%{__rm} $RPM_BUILD_ROOT%{_fontsdir}/FreeSans.ttf

%py_postclean

# cinepaint,cinepaint-script-fu,cinepaint-std-plugins domains
%find_lang cinepaint --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains only license notes
%doc AUTHORS BUGS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/cinepaint
%attr(755,root,root) %{_bindir}/cinepaint-remote
%attr(755,root,root) %{_libdir}/libcinepaint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaint.so.1
%attr(755,root,root) %{_libdir}/libcinepaintHalf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaintHalf.so.1
%attr(755,root,root) %{_libdir}/libcinepaint_fl_i18n.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaint_fl_i18n.so.1
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{abiver}
%dir %{_libdir}/%{name}/%{abiver}/extra
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/extra/dcraw
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/extra/jhead
%dir %{_libdir}/%{name}/%{abiver}/plug-ins
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/*
# resource directories
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{abiver}
%{_datadir}/%{name}/%{abiver}/brushes
%{_datadir}/%{name}/%{abiver}/curves
%{_datadir}/%{name}/%{abiver}/gradients
%{_datadir}/%{name}/%{abiver}/iol
%{_datadir}/%{name}/%{abiver}/palettes
%{_datadir}/%{name}/%{abiver}/patterns
%{_datadir}/%{name}/%{abiver}/scripts
# default rc(?)
%{_datadir}/%{name}/%{abiver}/gimprc
%{_datadir}/%{name}/%{abiver}/gimprc_user
%{_datadir}/%{name}/%{abiver}/gtkrc
%{_datadir}/%{name}/%{abiver}/gtkrc.forest2
%{_datadir}/%{name}/%{abiver}/printrc_user
%{_datadir}/%{name}/%{abiver}/ps-menurc
%{_datadir}/%{name}/%{abiver}/spot.splash.ppm
%{_datadir}/%{name}/%{abiver}/tips.txt
%attr(755,root,root) %{_datadir}/%{name}/%{abiver}/user_install
%attr(755,root,root) %{py_sitedir}/gimpmodule.so
%{py_sitescriptdir}/gimpenums.py[co]
%{py_sitescriptdir}/gimpfu.py[co]
%{py_sitescriptdir}/gimpplugin.py[co]
%{py_sitescriptdir}/gimpshelf.py[co]
%{py_sitescriptdir}/gimpui.py[co]
%{_mandir}/man1/cinepaint.1*
%{_desktopdir}/cinepaint.desktop
%{_pixmapsdir}/cinepaint.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cinepainttool
%attr(755,root,root) %{_libdir}/libcinepaint.so
%attr(755,root,root) %{_libdir}/libcinepaintHalf.so
%attr(755,root,root) %{_libdir}/libcinepaint_fl_i18n.so
%{_libdir}/libcinepaint.la
%{_libdir}/libcinepaintHalf.la
%{_libdir}/libcinepaint_fl_i18n.la
%{_includedir}/cinepaint
%{_pkgconfigdir}/cinepaint-gtk.pc
%{_aclocaldir}/cinepaint.m4
%{_mandir}/man1/cinepainttool.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcinepaint.a
%{_libdir}/libcinepaintHalf.a
%{_libdir}/libcinepaint_fl_i18n.a
