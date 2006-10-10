#
# TODO:
#      - Correct building with --with print
#
# Conditional build:
%bcond_with   print	# build with libgutenprintui

%define		subrel	1
%define		rel	1
%define		ver	0.21
%define		src	%{ver}-%{rel}
%define		fsrc	%{ver}-%{rel}-%{subrel}
Summary:	CinePaint - a motion picture editing tool
Summary(pl):	CinePaint - narz�dzie do obr�bki film�w
Name:		cinepaint
Version:	%{ver}_%{rel}
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/cinepaint/%{name}-%{src}.tar.gz
# Source0-md5:	d10b7e8c64209d32f665785f7c63da6e
%{?with_print:Patch0:		%{name}-gutenprintui.patch}
URL:		http://www.cinepaint.org/
BuildRequires:	OpenEXR-devel
BuildRequires:	automake
BuildRequires:	fltk-devel
BuildRequires:	giflib-devel
BuildRequires:	gtk+-devel
BuildRequires:	lcms-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
%{?with_print:BuildRequires:     libgutenprintui-devel}
Obsoletes:	filmgimp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CinePaint is a motion picture editing tool primarily used for painting
and retouching of movies. CinePaint is the most successful open source
tool in future motion picture work today. It was formerly known as
FilmGimp.

%description -l pl
CinePaint jest narz�dziem do obr�bki ruchomego obrazu, u�ywanym
g��wnie do rysowania i retuszu film�w. Na dzie� dzisiejszy jest
narz�dziem z otwartymi �r�d�ami, kt�re odnios�o najwi�kszy sukces w
bran�y filmowej. Wcze�niej by�o znane pod nazw� FilmGimp.

%package devel
Summary:	Header files for CinePaint libraries
Summary(pl):	Pliki nag��wkowe bibliotek CinePainta
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	filmgimp-devel

%description devel
Header files for CinePaint libraries.

%description devel -l pl
Pliki nag��wkowe bibliotek CinePainta.

%package static
Summary:	Static CinePaint libraries
Summary(pl):	Statyczne biblioteki CinePaint
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	filmgimp-static

%description static
Static CinePaint libraries.

%description static -l pl
Statyczne biblioteki CinePainta.

%prep
%setup -q -n %{name}-%{src}
%{?with_print:%patch0 -p1}

%build
cp -f /usr/share/automake/config.sub .
%configure \
	   %{!?with_print:--disable-print}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

%find_lang cinepaint --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
#%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{src}
%dir %{_libdir}/%{name}/%{src}/plug-ins
%attr(755,root,root) %{_libdir}/%{name}/%{src}/plug-ins/*
# resource directories
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{src}
%{_datadir}/%{name}/%{src}/brushes
%{_datadir}/%{name}/%{src}/gradients
%{_datadir}/%{name}/%{src}/palettes
%{_datadir}/%{name}/%{src}/patterns
%{_datadir}/%{name}/%{src}/curves
# default rc(?)
%{_datadir}/%{name}/%{src}/gimprc*
%{_datadir}/%{name}/%{src}/gtkrc*
%{_datadir}/%{name}/%{src}/ps-menurc
%attr(755,root,root) %{_datadir}/%{name}/%{src}/user_install
# other
%{_mandir}/man1/*.1*
%{_desktopdir}/cinepaint.desktop
%{_pixmapsdir}/cinepaint.png
%{_datadir}/%{name}/%{src}/*.ppm

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/cinepaint/*
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/cinepaint-gtk.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a