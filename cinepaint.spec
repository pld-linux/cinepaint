%define		rel	3
%define		ver	0.18
%define		src	%{ver}-%{rel}
Summary:	CinePaint - a motion picture editing tool
Summary(pl):	CinePaint - narzêdzie do obróbki filmów
Name:		cinepaint
Version:	%{ver}_%{rel}
Release:	4
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{src}.tar.gz
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

%description devel
Header files for CinePaint libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek CinePainta.

%package static
Summary:	Static CinePaint libraries
Summary(pl):	Statyczne biblioteki CinePaint
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CinePaint libraries.

%description static -l pl
Statyczne biblioteki CinePainta.

%prep
%setup -q -n %{name}-%{src}
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
#%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}/%{src}/
%dir %{_libdir}/%{name}/%{src}/plug-ins/
%{_libdir}/%{name}/%{src}/plug-ins/*
%attr(755,root,root) %{_libdir}/%{name}/%{src}/plug-ins/*
%dir %{_datadir}/%{name}/%{src}/
%dir %{_datadir}/%{name}/%{src}/*
# resource directories
%{_datadir}/%{name}/%{src}/brushes/*
%{_datadir}/%{name}/%{src}/gradients/*
%{_datadir}/%{name}/%{src}/palettes/*
%{_datadir}/%{name}/%{src}/patterns/*
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
