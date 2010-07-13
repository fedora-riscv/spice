Name:           spice
Version:        0.5.2
Release:        4%{?dist}
Summary:        Implements the SPICE protocol
Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://www.spice-space.org/
Source0:        http://www.spice-space.org/download/releases/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:  i686 x86_64

BuildRequires:  pkgconfig
BuildRequires:  spice-protocol
BuildRequires:  celt051-devel
BuildRequires:  pixman-devel alsa-lib-devel openssl-devel libjpeg-devel
BuildRequires:  libXrandr-devel

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

%package client
Summary:        Implements the client side of the SPICE protocol
Group:          User Interface/Desktops

%description client
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the SPICE client application.

%package server
Summary:        Implements the server side of the SPICE protocol
Group:          System Environment/Libraries

%description server
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the run-time libraries for any application that wishes
to be a SPICE server.

%package server-devel
Summary:        Header files, libraries and development documentation for spice-server
Group:          Development/Libraries
Requires:       %{name}-server = %{version}-%{release}
Requires:       pkgconfig

%description server-devel
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.

%prep
%setup -q -n spice-%{version}

%build
%configure
make -C client %{?_smp_mflags}
%ifarch x86_64
make %{?_smp_mflags}
%endif

%install
make DESTDIR=%{buildroot} -C client install
%ifarch x86_64
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
%endif

%files client
%defattr(-, root, root)
%doc COPYING README NEWS
%{_bindir}/spicec

%ifarch x86_64

%files server
%defattr(-, root, root)
%doc COPYING README NEWS
%{_libdir}/libspice-server.so.1
%{_libdir}/libspice-server.so.1.0.0

%post server -p /sbin/ldconfig

%postun server -p /sbin/ldconfig

%files server-devel
%defattr(-, root, root)
%doc COPYING README NEWS
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc

%endif

%changelog
* Tue Jul 13 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-4
- Quote %% in changelog to avoid macro expansion.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-3
- %%configure handles CFLAGS automatically, no need to fiddle
  with %%{optflags} manually.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-2
- Fix license: LGPL.
- Cleanup specfile, drop bits not needed any more with
  recent rpm versions (F13+).
- Use optflags as-is.
- 

* Fri Jul 9 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-1
- initial package.

