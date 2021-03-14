Summary:	DNF plugin to enable Copy on Write in RPM
Name:		dnf-plugin-cow
Version:	0.0.2
Release:	1
License:	MIT
Source0:	https://github.com/facebookincubator/dnf-plugin-cow/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b2e556a55d84c18484b4d0fb99a17865
URL:		https://github.com/facebookincubator/dnf-plugin-cow
BuildRequires:	dnf >= 4.2.23
BuildRequires:	python3-modules
Requires:	/usr/bin/rpm2extents
Requires:	dnf >= 4.2.23
Requires:	rpm-plugin-reflink
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Installing this package enables a DNF plugin which changes the
behaviour of librepo. Instead of downloading rpm files directly into
cache before installation they will be "transcoded" into "extent
based" rpms which contain all the constituent files of the rpm already
uncompressed. This package depends on a version of rpm which includes
/usr/bin/rpm2extents and the sub-package rpm-plugin-reflink which
understands these "extent based" rpms and can install files without
copying the underlying data.

This package broadly assumes the root filesystem supports copy on
write / reflink'ing. Today this means btrfs or xfs.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dnf/plugins \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/dnf-plugins

cp -p reflink.conf $RPM_BUILD_ROOT%{_sysconfdir}/dnf/plugins/reflink.conf
cp -p reflink.py $RPM_BUILD_ROOT%{py3_sitescriptdir}/dnf-plugins/reflink.py

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}/dnf-plugins
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}/dnf-plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md
%config(noreplace) %{_sysconfdir}/dnf/plugins/reflink.conf
%{py3_sitescriptdir}/dnf-plugins/reflink.py
%{py3_sitescriptdir}/dnf-plugins/__pycache__/reflink.*
