#
#
Summary:	CinePaint - A Motion picture editing tool
Summary(pl):	CinePaint - Narz�dzie do obr�bki film�w
Name:		cinepaint
Version:	0.18
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}-1.tar.gz
# Source0-md5:	96fb1fb6e71b24b6e743376c0c9d5896
Patch0:		%{name}-gcc3.patch
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
Film Gimp is a motion picture editing tool primarily used for painting
and retouching of movies. Film Gimp is the most successful open source
tool in future motion picture work today.

%description -l pl
Film Gimp jest narz�dziem do obr�bki ruchomego obrazu, u�ywanym
g��wnie do rysowania i retuszu film�w. Na dzie� dzisiejszy jest
narz�dziem z otwartymi �r�d�ami, kt�re odnios�o najwi�kszy sukces w
bran�y filmowej.

%package devel
Summary:	Header files for filmgimp libraries
Summary(pl):	Pliki nag��wkowe bibliotek filmgimpa
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for filmgimp libraries.

%description devel -l pl
Pliki nag��wkowe bibliotek filmgimpa.

%package static
Summary:	Static filmgimp libraries
Summary(pl):	Statyczne biblioteki filmgimpa
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static filmgimp libraries.

%description static -l pl
Statyczne biblioteki filmgimpa.

%prep
%setup -q
%patch0 -p1

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
