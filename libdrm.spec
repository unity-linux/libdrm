%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define major 2
%define libname %mklibname drm %{major}
%define develname %mklibname drm -d

%define kms_major 1
%define libkms %mklibname kms %{kms_major}
%define intel_major 1
%define libintel %mklibname drm_intel %{intel_major}
%define nouveau_major 2
%define libnouveau %mklibname drm_nouveau %{nouveau_major}
%define radeon_major 1
%define libradeon %mklibname drm_radeon %{radeon_major}
%define tegra_major 0
%define libtegra %mklibname drm_tegra %{tegra_major}
%define omap_major 1
%define libomap %mklibname drm_omap %{omap_major}
%define exynos_major 1
%define libexynos %mklibname drm_exynos %{exynos_major}
%define freedreno_major 1
%define libfreedreno %mklibname drm_freedreno %{freedreno_major}
%define amdgpu_major 1
%define libamdgpu %mklibname drm_amdgpu %{amdgpu_major}

Name:		libdrm
Summary:        Direct Rendering Manager runtime library
Version:	2.4.83
Release:	%mkrel 2
License:        MIT
Group:		System/Libraries
URL:		http://xorg.freedesktop.org
Source0:	http://dri.freedesktop.org/libdrm/libdrm-%{version}.tar.bz2
Source2:	91-drm-modeset.rules

BuildRequires:  pkgconfig 
BuildRequires:  automake 
BuildRequires:  autoconf 
BuildRequires:  libtool
BuildRequires:	kernel-userspace-headers >= 3.3.1-1
BuildRequires:	libpthread-stubs
BuildRequires:	x11-util-macros >= 1.0.1
%if !%bootstrap
BuildRequires:  pkgconfig(systemd)
%endif
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	xsltproc
BuildRequires:	docbook-xsl
%ifnarch %arm %mips
BuildRequires:	pkgconfig(valgrind)
%endif
BuildRequires:	pkgconfig(cunit)
BuildRequires:	pkgconfig(udev)

# Upstream fixes
Patch0001:	tests-amdgpu-add-missing-header-to-SOURCES.patch
# (tmb) not really upstream, but is added because of P1
Patch0002:	tests-amdgpu-add-missng-uve_ib.h.patch

# Fedora patches:
# hardcode the 666 instead of 660 for device nodes
Patch0101:	libdrm-make-dri-perms-okay.patch
# remove backwards compat not needed on Fedora
Patch0102:	libdrm-2.4.69-no-bc.patch
# make rule to print the list of test programs
Patch0103:	libdrm-2.4.25-check-programs.patch

Patch0500:	0500-improve-waiting-for-dri-device-to-appear-when-system.patch

%description
Direct Rendering Manager runtime library

%package common
Summary:	Common files for the userspace interface to kernel DRM services
Group:		System/Libraries

%description common
Common files for the userspace interface to kernel DRM services

%package -n	%{libname}
Summary:	Userspace interface to kernel DRM services
Group:		System/Libraries
Provides:	%{name} = %{version}
Requires: %{name}-common

%description -n	%{libname}
Userspace interface to kernel DRM services

%package -n %{libkms}
Summary:  Shared library for KMS
Group:    System/Libraries

%description -n %{libkms}
Shared library for kernel mode setting.

%ifarch %{ix86} x86_64
%package -n	%{libintel}
Summary:	Shared library for Intel kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libintel}
Shared library for Intel kernel Direct Rendering Manager services.
%endif

%package -n	%{libnouveau}
Summary:	Shared library for Nouveau kernel DRM services
Group:		System/Libraries

%description -n %{libnouveau}
Shared library for Nouveau kernel Direct Rendering Manager services.

%package -n	%{libradeon}
Summary:	Shared library for Radeon kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libradeon}
Shared library for Radeon kernel Direct Rendering Manager services.

%ifarch %arm
%package -n	%{libomap}
Summary:	Shared library for OMAP kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libomap}
Shared library for OMAP kernel Direct Rendering Manager services.

%package -n	%{libtegra}
Summary:	Shared library for TEGRA kernel DRM services
Group:		System/Libraries

%description -n %{libtegra}
Shared library for TEGRA kernel Direct Rendering Manager services.

%package -n	%{libexynos}
Summary:	Shared library for Exynos kernel DRM services
Group:		System/Libraries
Conflicts:	%{_lib}drm2 < 2.4.5-2

%description -n %{libexynos}
Shared library for EXYNOS kernel Direct Rendering Manager services.

%package -n	%{libfreedreno}
Summary:	Shared library for Freedreno kernel DRM services
Group:		System/Libraries

%description -n %{libfreedreno}
Shared library for Freedreno kernel Direct Rendering Manager services.

%endif

%package -n	%{libamdgpu}
Summary:	Shared library for AMDGPU kernel DRM services
Group:		System/Libraries

%description -n %{libamdgpu}
Shared library for AMDGPU kernel Direct Rendering Manager services.

%package -n	%{develname}
Summary:        Direct Rendering Manager development package
Group:		Development/X11
Requires:	%{libname} = %{version}
Requires:	%{libkms} = %{version}
%ifarch %{ix86} x86_64
Requires:	%{libintel} = %{version}
%endif
Requires:	%{libnouveau} = %{version}
Requires:	%{libradeon} = %{version}
Requires:	%{libamdgpu} = %{version}
%ifarch %arm
Requires:	%{libomap} = %{version}
Requires:	%{libtegra} = %{version}
Requires:	%{libexynos} = %{version}
Requires:	%{libfreedreno} = %{version}
%endif
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{mklibname drm 2 -d}
Obsoletes:	drm-nouveau-devel < 2.3.0-2.20090111.2

%description -n	%{develname}
Direct Rendering Manager development package.

%package -n drm-utils
Summary:        Direct Rendering Manager utilities
Group:		System/Base
Requires:       %{libname}%{?_isa} = %{version}-%{release}

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.

%prep
%autosetup -p1

%build
autoreconf -v --install || exit 1
%configure2_5x \
    --disable-vc4 \
%ifarch %{arm} aarch64
    --enable-exynos-experimental-api \
    --enable-tegra-experimental-api \
    --enable-vc4 \
    --enable-omap-experimental-api \
%endif
    --enable-install-test-programs \
    --enable-udev


%make_build V=1
pushd tests
%make_build `make check-programs` V=1
popd

%install
%make_install
pushd tests
mkdir -p %{buildroot}%{_bindir}
for foo in $(make check-programs) ; do
 libtool --mode=install install -m 0755 $foo %{buildroot}%{_bindir}
done
popd
mkdir -p %{buildroot}%{_udevrulesdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_udevrulesdir}

# NOTE: We intentionally don't ship *.la files
find %{buildroot} -type f -name "*.la" -delete

# (cg) Note that RH remove r300_reg.h via_3d_reg.h
# and we should perhaps do the same? (previous attempts have not gone well :)

%files common
%{_udevrulesdir}/91-drm-modeset.rules
%{_datadir}/libdrm/amdgpu.ids

%files -n %{libname}
%{_libdir}/libdrm.so.%{major}{,.*}

%files -n %{libkms}
%{_libdir}/libkms.so.%{kms_major}{,.*}

%ifarch %{ix86} x86_64
%files -n %{libintel}
%{_libdir}/libdrm_intel.so.%{intel_major}{,.*}
%endif

%files -n %{libnouveau}
%{_libdir}/libdrm_nouveau.so.%{nouveau_major}{,.*}

%files -n %{libamdgpu}
%{_libdir}/libdrm_amdgpu.so.%{amdgpu_major}{,.*}

%files -n %{libradeon}
%{_libdir}/libdrm_radeon.so.%{radeon_major}{,.*}

%ifarch %arm
%files -n %{libomap}
%{_libdir}/libdrm_omap.so.%{omap_major}{,.*}

%files -n %{libtegra}
%{_libdir}/libdrm_tegra.so.%{tegra_major}{,.*}

%files -n %{libexynos}
%{_libdir}/libdrm_exynos.so.%{exynos_major}{,.*}

%files -n %{libfreedreno}
%{_libdir}/libdrm_freedreno.so.%{freedreno_major}{,.*}
%endif

%files -n drm-utils
%{_bindir}/amdgpu_test
%{_bindir}/drmdevice
%{_bindir}/modetest
%{_bindir}/modeprint
%{_bindir}/vbltest
%{_bindir}/kmstest
%{_bindir}/kms-steal-crtc
%{_bindir}/kms-universal-planes
%exclude %{_bindir}/exynos*
%exclude %{_bindir}/drmsl
%exclude %{_bindir}/hash
%exclude %{_bindir}/proptest
%exclude %{_bindir}/random

%files -n %{develname}
%{_includedir}/libdrm
%{_includedir}/libkms
%{_includedir}/*.h
%ifarch %arm
%{_includedir}/omap/*.h
%{_includedir}/exynos/*.h
%{_includedir}/freedreno/*.h
%endif
%{_libdir}/libdrm*.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm*.pc
%{_libdir}/pkgconfig/libkms*.pc
%{_mandir}/man3/drmAvailable.3.xz
%{_mandir}/man3/drmHandleEvent.3.xz
%{_mandir}/man3/drmModeGetResources.3.xz
%{_mandir}/man7/drm-gem.7.xz
%{_mandir}/man7/drm-kms.7.xz
%{_mandir}/man7/drm-memory.7.xz
%{_mandir}/man7/drm-mm.7.xz
%{_mandir}/man7/drm-ttm.7.xz
%{_mandir}/man7/drm.7.xz
