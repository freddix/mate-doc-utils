Summary:	Documentation utilities for MATE
Name:		mate-doc-utils
Version:	1.6.2
Release:	2
License:	GPL v2+/LGPL v2+
Group:		Development/Tools
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	6bbbe07b54404a5bbe19e5d21e21aebe
Patch0:		%{name}-no_scrollkeeper_update.patch
URL:		http://wiki.mate-desktop.org/mate-doc-utils
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	python
BuildRequires:	rarian-devel
Requires(post,postun):	rarian
Requires:	gnome-doc-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		_pkgconfigdir		%{_datadir}/pkgconfig

%description
Collection of documentation utilities for MATE.

%prep
%setup -q
%patch0 -p1

%build
rm aclocal.m4
%{__intltoolize}
%{__aclocal} -I tools -I m4
%{__automake}
%{__autoconf}
%configure \
	--build=%{_host}	\
	--host=%{_host}		\
	--disable-scrollkeeper
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove unnecessary python sitepackages provided by gnome-doc-utils
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/*
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man1/*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/xml/mallard
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/xml2po
%{__rm} -r $RPM_BUILD_ROOT%{_npkgconfigdir}/xml2po.pc

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}
%find_lang %{name} --all-name --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post

%postun
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-*
%{_aclocaldir}/mate*.m4
%{_datadir}/mate-doc-utils
%{_datadir}/xml/mate
%{_npkgconfigdir}/mate-doc-utils.pc

