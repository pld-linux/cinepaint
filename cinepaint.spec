Summary:	CinePaint - a motion picture editing tool
Summary(pl):	CinePaint - narzêdzie do obróbki filmów
Name:		cinepaint
Version:	0.18
Release:	3
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}-3.tar.gz
# Source0-md5:	0bee7d7fc8f352ddbcc6f4720ecc14cc
##Patch0:		%{name}-gcc3.patch
URL:		http://cinepaint.sourceforge.net/
BuildRequires:	automake
BuildRequires:	gtk+-devel >= 1.2.8
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libungif-devel
BuildRequires:	zlib-devel
Obsoletes:	filmgimp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CinePaint is a motion picture editing tool primarily used for painting
and retouching of movies. CinePaint is the most successful open source
tool in future motion picture work today. It was formerly known as
FilmGimp.

%description -l pl
CinePaint jest narzêdziem do obróbki ruchomego obrazu, u¿ywanym
g³ównie do rysowania i retuszu filmów. Na dzieñ dzisiejszy jest
narzêdziem z otwartymi ¼ród³ami, które odnios³o najwiêkszy sukces w
bran¿y filmowej. Wcze¶niej by³o znane pod nazw± FilmGimp.

%package devel
Summary:	Header files for CinePaint libraries
Summary(pl):	Pliki nag³ówkowe bibliotek CinePainta
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	filmgimp-devel

%description devel
Header files for CinePaint libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek CinePainta.

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
%setup -q
##%%patch0 -p1

%build
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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/filmgimp
%dir %{_datadir}/filmgimp
%dir %{_datadir}/filmgimp/*
# resource directories
%{_datadir}/filmgimp/*/brushes
%{_datadir}/filmgimp/*/gradients
%{_datadir}/filmgimp/*/palettes
%{_datadir}/filmgimp/*/patterns
%{_datadir}/filmgimp/*/scripts
# default rc(?)
%{_datadir}/filmgimp/*/gimprc*
%{_datadir}/filmgimp/*/gtkrc*
%{_datadir}/filmgimp/*/ps-menurc
# other
%{_datadir}/filmgimp/*/gimp_*.ppm
%{_datadir}/filmgimp/*/gimp_tips.txt
%attr(755,root,root) %{_datadir}/filmgimp/*/user_install
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/filmgimp*
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
