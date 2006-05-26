%define		subrel	1
%define		rel	1
%define		ver	0.19
%define		src	%{ver}-%{rel}
%define		fsrc	%{ver}-%{rel}-%{subrel}
Summary:	CinePaint - a motion picture editing tool
Summary(pl):	CinePaint - narz�dzie do obr�bki film�w
Name:		cinepaint
Version:	%{ver}_%{rel}
Release:	0.3
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/cinepaint/%{name}-%{fsrc}.tar.gz
# Source0-md5:	bfd8c21724631d157097927cf3020277
##Patch0:		%{name}-gcc3.patch
URL:		http://cinepaint.sourceforge.net/
BuildRequires:	OpenEXR-devel
BuildRequires:	automake
BuildRequires:	giflib-devel
BuildRequires:	gtk+-devel
BuildRequires:	lcms-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
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
##%%patch0 -p1

%build
cp -f /usr/share/automake/config.sub .
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
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
#%{_datadir}*/scripts
# default rc(?)
%{_datadir}/%{name}/%{src}/gimprc*
%{_datadir}/%{name}/%{src}/gtkrc*
%{_datadir}/%{name}/%{src}/ps-menurc
%attr(755,root,root) %{_datadir}/%{name}/%{src}/user_install
# other
#%{_datadir}/filmgimp/*/gimp_*.ppm
#%{_datadir}/filmgimp/*/gimp_tips.txt
#%attr(755,root,root) %{_datadir}/filmgimp/*/user_install
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
#%{_includedir}/filmgimp*
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a