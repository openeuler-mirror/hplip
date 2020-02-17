Name: hplip
Summary: HP Linux Imaging and Printing Project
Version: 3.18.6
Release: 9
License: GPLv2+ and MIT and BSD and IJG and Public Domain and GPLv2+ with exceptions and ISC
Url: https://developers.hp.com/hp-linux-imaging-and-printing
Source0: http://downloads.sourceforge.net/sourceforge/hplip/hplip-%{version}.tar.gz
Source1: hpcups-update-ppds.sh
Source2: copy-deviceids.py
Source3: hplip.appdata.xml

Patch1: hplip-pstotiff-is-rubbish.patch
Patch3: hplip-ui-optional.patch
Patch5: hplip-deviceIDs-drv.patch
Patch6: hplip-udev-rules.patch
Patch7: hplip-retry-open.patch
Patch8: hplip-snmp-quirks.patch
Patch9: hplip-hpijs-marker-supply.patch
Patch10: hplip-clear-old-state-reasons.patch
Patch11: hplip-hpcups-sigpipe.patch
Patch12: hplip-logdir.patch
Patch13: hplip-bad-low-ink-warning.patch
Patch14: hplip-deviceIDs-ppd.patch
Patch15: hplip-ppd-ImageableArea.patch
Patch16: hplip-scan-tmp.patch
Patch17: hplip-log-stderr.patch
Patch18: hplip-avahi-parsing.patch
Patch20: hplip-dj990c-margin.patch
Patch21: hplip-strncpy.patch
Patch22: hplip-no-write-bytecode.patch
Patch23: hplip-silence-ioerror.patch
Patch24: hplip-3165-sourceoption.patch
Patch25: hplip-noernie.patch
Patch27: hplip-check-cups.patch
Patch30: hplip-typo.patch
Patch31: hplip-use-binary-str.patch
Patch32: hplip-colorlaserjet-mfp-m278-m281.patch
Patch33: hplip-error-print.patch
Patch34: hplip-hpfax-importerror-print.patch

Requires: python3-pillow python3-gobject cups python3-dbus systemd %{_bindir}/gpg
Requires: python3-qt5 wget python3-gobject python3-reportlab sane-backends python3

BuildRequires: autoconf automake libtool net-snmp-devel cups-devel libappstream-glib
BuildRequires: gcc python3-devel libjpeg-devel desktop-file-utils libusb1-devel systemd
BuildRequires: gcc-c++ openssl-devel sane-backends-devel pkgconfig(dbus-1) cups python3-cups

Obsoletes: hpijs < 1:%{version}-%{release}
Provides:  hpijs = 1:%{version}-%{release}

Obsoletes: libsane-hpoj < 0.91
Provides: libsane-hpoj = 0.91

Obsoletes: %{name}-compat-libs < %{version}-%{release}

Obsoletes: hplip-common < %{version}-%{release}
Provides:  hplip-common = %{version}-%{release}
Obsoletes: hplip-libs < %{version}-%{release}
Provides:  hplip-libs = %{version}-%{release}
Obsoletes: hplip-gui < %{version}-%{release}
Provides:  hplip-gui = %{version}-%{release}
Obsoletes: libsane-hpaio < %{version}-%{release}
Provides:  libsane-hpaio = %{version}-%{release}

%description
The Hewlett-Packard Linux Imaging and Printing Project provides
drivers for HP printers and multi-function peripherals.

%package_help

%prep
%setup -q

%patch1 -p1 -b .pstotiff-is-rubbish
%patch3 -p1 -b .ui-optional
%patch5 -p1 -b .deviceIDs-drv
chmod +x %{SOURCE2}
mv prnt/drv/hpijs.drv.in{,.deviceIDs-drv-hpijs}
%{SOURCE2} prnt/drv/hpcups.drv.in \
           prnt/drv/hpijs.drv.in.deviceIDs-drv-hpijs \
           > prnt/drv/hpijs.drv.in

%patch6 -p1 -b .udev-rules
%patch7 -p1 -b .retry-open
%patch8 -p1 -b .snmp-quirks
%patch9 -p1 -b .hpijs-marker-supply
%patch10 -p1 -b .clear-old-state-reasons
%patch11 -p1 -b .hpcups-sigpipe
%patch12 -p1 -b .logdir
%patch13 -p1 -b .bad-low-ink-warning

for ppd_file in $(grep '^diff' %{PATCH14} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch14 -p1 -b .deviceIDs-ppd
for ppd_file in $(grep '^diff' %{PATCH14} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

for ppd_file in $(grep '^diff' %{PATCH15} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch15 -p1 -b .ImageableArea
for ppd_file in $(grep '^diff' %{PATCH15} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

%patch16 -p1 -b .scan-tmp
%patch17 -p1 -b .log-stderr
%patch18 -p1 -b .parsing
%patch20 -p1 -b .dj990c-margin
%patch21 -p1 -b .strncpy
%patch22 -p1 -b .no-write-bytecode
%patch23 -p1 -b .silence-ioerror
%patch24 -p1 -b .sourceoption
%patch25 -p1 -b .no-ernie

rm prnt/hpcups/ErnieFilter.{cpp,h} prnt/hpijs/ernieplatform.h

%patch27 -p1 -b .check-cups
%patch30 -p1 -b .typo

%patch31 -p1 -b .use-binary-str
%patch32 -p1 -b .colorlaserjet-mfp-m278-m281
%patch33 -p1 -b .error-print-fix
%patch34 -p1 -b .hpfax-import-error-print

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

find -name '*.py' -print0 | xargs -0 \
    sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python3},'
sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python3},' \
    prnt/filters/hpps \
    fax/filters/pstotiff

rm locatedriver

%build

sed -i 's|^AM_INIT_AUTOMAKE|AM_INIT_AUTOMAKE([foreign])|g' configure.in

autoreconf --verbose --force --install

%configure \
        --enable-scan-build --enable-gui-build --enable-fax-build \
        --disable-foomatic-rip-hplip-install --enable-pp-build \
        --disable-qt4 --enable-qt5 --enable-hpcups-install \
        --enable-cups-drv-install --enable-foomatic-drv-install \
        --enable-hpijs-install --disable-policykit \
        --with-mimedir=%{_datadir}/cups/mime PYTHON=%{__python3}

%make_build

%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
%make_install DESTDIR=${RPM_BUILD_ROOT} PYTHON=%{__python3}

install -d ${RPM_BUILD_ROOT}/run/hplip
install -d ${RPM_BUILD_ROOT}%{_sharedstatedir}/hp
install -d ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/hplip.conf <<EOF

d /run/hplip 0775 root lp -
EOF

install -d ${RPM_BUILD_ROOT}%{_datadir}/appdata
cp -a %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/appdata/
install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/{16x16,32x32,64x64}/apps

pushd ${RPM_BUILD_ROOT}%{_datadir}
install -p -m644 hplip/data/images/16x16/hp_logo.png icons/hicolor/16x16/apps/hp_logo.png
install -p -m644 hplip/data/images/32x32/hp_logo.png icons/hicolor/32x32/apps/hp_logo.png
install -p -m644 hplip/data/images/64x64/hp_logo.png icons/hicolor/64x64/apps/hp_logo.png
popd

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications
sed -i -e '/^Categories=/d' hplip.desktop
sed -i -e '/^Encoding=/d' hplip.desktop
desktop-file-validate hplip.desktop
desktop-file-install --vendor HP --dir ${RPM_BUILD_ROOT}/%{_datadir}/applications --add-category System \
                     --add-category Settings --add-category HardwareSettings hplip.desktop
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/appdata/*.appdata.xml
install -p -m755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/hpcups-update-ppds
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sane.d/dll.d
echo hpaio > ${RPM_BUILD_ROOT}%{_sysconfdir}/sane.d/dll.d/hpaio
find doc/images -type f -exec chmod 644 {} \;
install -d ${RPM_BUILD_ROOT}%{_datadir}/hplip/prnt/plugins

%pre
%{_bindir}/systemctl start cups &>/dev/null ||:
%{_bindir}/systemctl enable cups &>/dev/null ||:

%post
%{_bindir}/hpcups-update-ppds &>/dev/null ||:
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc COPYING doc/*
%license COPYING
%{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data
%{_datadir}/%{name}/*
%{_datadir}/cups/*
%{_datadir}/cups/mime/pstotiff.convs
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/ppd
%{_libdir}/*so*
%{_libdir}/sane/*so*
%{python3_sitearch}/*
%{_cups_serverbin}/backend/*
%{_cups_serverbin}/filter/*
%{_tmpfilesdir}/%{name}.conf
%{_udevrulesdir}/56-hpmud.rules
%{_sharedstatedir}/hp
%dir %attr(0775,root,lp) /run/%{name}
%dir %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/hp/%{name}.conf
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio

%exclude %{_datadir}/%{name}/doctor.pyc
%exclude %{_datadir}/%{name}/doctor.pyo
%exclude %{_datadir}/%{name}/logcapture.pyc
%exclude %{_datadir}/%{name}/logcapture.pyo
%exclude %{_datadir}/%{name}/pkservice.pyc
%exclude %{_datadir}/%{name}/pkservice.pyo
%exclude %{_datadir}/%{name}/pqdiag.pyc
%exclude %{_datadir}/%{name}/pqdiag.pyo
%exclude %{_datadir}/%{name}/hpaio.desc
%exclude %{_datadir}/%{name}/%{name}-install
%exclude %{_datadir}/%{name}/install.*
%exclude %{_datadir}/%{name}/uninstall.*
%exclude %{_datadir}/%{name}/pkservice.py
%exclude %{_datadir}/%{name}/locatedriver*
%exclude %{_datadir}/%{name}/dat2drv*
%exclude %{_datadir}/%{name}/logcapture.py
%exclude %{_datadir}/%{name}/doctor.py
%exclude %{_datadir}/%{name}/pqdiag.py
%exclude %{_datadir}/%{name}/hpijs.drv.in.template
%exclude %{_datadir}/%{name}/fax/pstotiff*
%exclude %{_datadir}/%{name}/upgrade.*
%exclude %{_datadir}/hal/fdi
%exclude %{_datadir}/applications/%{name}.desktop
%exclude %{_datadir}/cups/mime/pstotiff.types
%exclude %{_docdir}
%exclude %{_bindir}/hp-pkservice
%exclude %{_bindir}/hp-logcapture
%exclude %{_bindir}/hp-doctor
%exclude %{_bindir}/hp-pqdiag
%exclude %{_bindir}/hp-uninstall
%exclude %{_bindir}/hp-upgrade
%exclude %{_libdir}/*.la
%exclude %{_libdir}/libhpip.so
%exclude %{_libdir}/libhpipp.so
%exclude %{_libdir}/libhpdiscovery.so
%exclude %{_libdir}/sane/*.la
%exclude %{_unitdir}/%{name}-printer@.service
%exclude %{_sysconfdir}/xdg/autostart/%{name}-systray.desktop
%exclude %{_sysconfdir}/sane.d
%exclude %{python3_sitearch}/*.la

%changelog
* Wed Nov 27 2019 caomeng<caomeng5@huawei.com> -  3.18.6-9
- Package init
