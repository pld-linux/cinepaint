#
# Conditional build:
%bcond_without	gutenprint	# gutenprint-based print plugin
%bcond_with	gtk1		# GTK+ 1.x instead of 2.x

Summary:	CinePaint - a motion picture editing tool
Summary(pl.UTF-8):	CinePaint - narzędzie do obróbki filmów
Name:		cinepaint
Version:	1.3
Release:	12
License:	GPL v2+ (with LGPL v2.1+ and MIT parts)
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/cinepaint/%{name}-%{version}.tgz
# Source0-md5:	f8ecd5671662e71a3356213de371fee4
Patch0:		%{name}-am.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-libpng.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-paths.patch
Patch5:		%{name}-libdir.patch
Patch6:		%{name}-oyranos.patch
Patch7:		%{name}-format.patch
Patch8:		%{name}-include.patch
Patch9:		%{name}-python.patch
Patch10:	%{name}-extern.patch
Patch11:	%{name}-no-common.patch
Patch12:	%{name}-ptr.patch
Patch13:	%{name}-gcc.patch
URL:		http://cinepaint.org/
BuildRequires:	OpenEXR-devel >= 1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	fltk-gl-devel
BuildRequires:	gettext-tools
%if %{with gtk1}
BuildRequires:	glib-devel
BuildRequires:	gtk+-devel >= 1.2.8
%else
BuildRequires:	gtk+2-devel >= 2.0.0
%endif
BuildRequires:	lcms-devel >= 1.16
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	oyranos-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
%{?with_gutenprint:BuildRequires:	libgutenprintui-devel >= 5.0.0}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	OpenEXR >= 1.0.0
# FreeSans.ttf
Requires:	fonts-TTF-freefont
Requires:	lcms >= 1.16
Obsoletes:	filmgimp < 1
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

%package libs
Summary:	CinePaint shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone CinePainta
Group:		Libraries
%if %{with gtk1}
Requires:	gtk+ >= 1.2.8
%endif
Conflicts:	cinepaint < 1.3

%description libs
CinePaint shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone CinePainta.

%package devel
Summary:	Header files for CinePaint libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek CinePainta
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%if %{with gtk1}
Requires:	gtk+-devel >= 1.2.8
%else
Requires:	gtk+2-devel >= 2.0.0
%endif
Obsoletes:	filmgimp-devel < 1

%description devel
Header files for CinePaint libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek CinePainta.

%package static
Summary:	Static CinePaint libraries
Summary(pl.UTF-8):	Statyczne biblioteki CinePaint
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	filmgimp-static < 1

%description static
Static CinePaint libraries.

%description static -l pl.UTF-8
Statyczne biblioteki CinePainta.

%package plugin-print
Summary:	Print plug-in for CinePaint
Summary(pl.UTF-8):	Wtyczka do drukowania dla CinePainta
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgutenprintui >= 5.0.0

%description plugin-print
Print plug-in for CinePaint.

%description plugin-print -l pl.UTF-8
Wtyczka do drukowania dla CinePainta.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

# dead symlinks
%{__rm} config.guess config.sub py-compile

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' plug-ins/pygimp/plug-ins/*.py

%build
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__automake}
%configure \
	%{!?with_gutenprint:--disable-print}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

# referenced by float16.h, but not installed
install -d $RPM_BUILD_ROOT%{_includedir}/cinepaint/libhalf
cp -p libhalf/cinepaint_half.h $RPM_BUILD_ROOT%{_includedir}/cinepaint/libhalf

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gimpmodule.{la,a}
# provided by fonts-TTF-freefont
%{__rm} $RPM_BUILD_ROOT%{_fontsdir}/FreeSans.ttf

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{no,nb}

# cinepaint,cinepaint-script-fu,cinepaint-std-plugins domains
%find_lang cinepaint --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains only license notes
%doc AUTHORS BUGS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/cinepaint
%attr(755,root,root) %{_bindir}/cinepaint-remote
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{abiver}
%dir %{_libdir}/%{name}/%{abiver}/extra
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/extra/dcraw
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/extra/jhead
%dir %{_libdir}/%{name}/%{abiver}/plug-ins
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/blur
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/bmp
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/bracketing_to_hdr
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/cineon
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/clothify.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/collect
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/compose
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/dbbrowser
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/decompose
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/dicom
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/edge
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/fits
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/foggify.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/gauss_rle
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/gbr
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/gifload
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/gimpcons.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/gtkcons.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/hdr
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/icc_examin_cp
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/iff
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/iol
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/jpeg
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/mblur
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/median
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/minimum
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/noisify
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/openexr
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/pdbbrowse.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/pdf
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/pic
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/png
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/pnm
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/psd
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/psd_save
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/rawphoto
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/retinex
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/rotate
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/screenshot
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/script-fu
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/sgi
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/shadow_bevel.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/sharpen
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/snoise
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/sobel
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/sphere.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/spread
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/tga
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/tiff
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/unsharp
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/whirlpinch.py
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/xwd
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

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcinepaint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaint.so.1
%attr(755,root,root) %{_libdir}/libcinepaintHalf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaintHalf.so.1
%attr(755,root,root) %{_libdir}/libcinepaint_fl_i18n.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinepaint_fl_i18n.so.1

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

%files plugin-print
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{abiver}/plug-ins/print
