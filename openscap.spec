%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           openscap
Version:        0.6.0
Release:        1%{?dist}
Summary:        Set of open source libraries enabling integration of the SCAP line of standards
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.open-scap.org/
Source0:        http://www.open-scap.org/download/%{name}-%{version}.tar.gz
# This works around some perl issue in RHEL6
Patch1:		openscap-0.6.0-perl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Remove next line when perl is fixed
BuildRequires:  autoconf, automake, libtool
BuildRequires:  swig libxml2-devel
BuildRequires:  rpm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pcre-devel
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
OpenSCAP is a set of open source libraries providing an easier path 
for integration of the SCAP line of standards. SCAP is a line of standards 
managed by NIST with the goal of providing a standard language 
for the expression of Computer Network Defense related information.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        python
Summary:        Python bindings for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python-devel 

%description    python
The %{name}-python package contains the bindings so that %{name}
libraries can be used by python.

%package        perl
Summary:        Perl bindings for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  perl-devel

%description    perl
The %{name}-perl package contains the bindings so that %{name}
libraries can be used by perl.

%package        utils
Summary:        Openscap utilities
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires(post):  chkconfig
Requires(preun): chkconfig initscripts
BuildRequires:   libcurl-devel

%description    utils
The %{name}-utils package contains various utilities based on %{name} library.

%prep
%setup -q
# Remove next line when perl is fixed
%patch1 -p1

%build
# Remove next line when perl is fixed
autoreconf -i -s
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 755 dist/fedora/oscap-scan.init $RPM_BUILD_ROOT%{_initrddir}/oscap-scan
install -p -m 644 dist/fedora/oscap-scan.sys  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/oscap-scan

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post utils
/sbin/chkconfig --add oscap-scan

%preun utils
if [ $1 -eq 0 ]; then
   /sbin/service oscap-scan stop > /dev/null 2>&1
   /sbin/chkconfig --del oscap-scan
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*
%{_libexecdir}/*
%{_datadir}/openscap/schemas/*

%files python
%defattr(-,root,root,-)
%{python_sitearch}/*

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%{perl_vendorlib}/*

%files devel
%defattr(-,root,root,-)
%doc docs/{html,latex,examples}/
%{_includedir}/*
%{_libdir}/*.so

%files utils
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/sysconfig/oscap-scan
%{_initrddir}/oscap-scan
%{_datadir}/openscap/oscap-scan.cron
%{_datadir}/openscap/scap-fedora12-oval.xml
%{_datadir}/openscap/scap-fedora13-oval.xml
%{_mandir}/man8/*
%{_bindir}/*


%changelog
* Wed Jul 14 2010 Peter Vrabec <pvrabec@redhat.com> 0.6.0-1
- rebase to upstream release
  Resolves: #565658, #599370

* Wed Jun 30 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.12-1
- Resolves: #565658 rebase to upstream release

* Wed May 26 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.11-1
- Resolves: #565658 rebase to upstream release

* Fri May 07 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.10-1
- Resolves: #565658 rebase to upstream release

* Fri Apr 16 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.9-1
- Resolves: #565658 rebase to upstream release

* Wed Mar 24 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.8-1
- Resolves: #565658 rebase to upstream release

* Fri Feb 26 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.7-1
- upgrade
- new utils package

* Mon Jan 04 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.6-1
- upgrade

* Tue Sep 29 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.3-1
- upgrade

* Wed Aug 19 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.2-1
- upgrade

* Mon Aug 03 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.1-2
- add rpm-devel requirement

* Mon Aug 03 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.1-1
- upgrade

* Thu Apr 30 2009 Peter Vrabec <pvrabec@redhat.com> 0.3.3-1
- upgrade

* Thu Apr 23 2009 Peter Vrabec <pvrabec@redhat.com> 0.3.2-1
- upgrade

* Sun Mar 29 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.4-1
- upgrade

* Fri Mar 27 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.3-2
- spec file fixes (#491892)

* Tue Mar 24 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.3-1
- upgrade

* Thu Jan 15 2009 Tomas Heinrich <theinric@redhat.com> 0.1.1-1
- Initial rpm

