%global debug_package %{nil}
%global __strip /bin/true

Name:           flutter
Version:        3.29.0
Release:        1%{?dist}
Summary:        Flutter SDK - Google's UI toolkit for building applications
License:        BSD
URL:            https://flutter.dev/

# For x86_64
Source0:        https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{version}-stable.tar.xz
# If you need different sources for arm64, add them here

# Adding required dependencies
BuildRequires:  unzip
BuildRequires:  chrpath
BuildRequires:  git
BuildRequires:  xz
Requires:       dart
Requires:       git
Requires:       clang
Requires:       cmake
Requires:       ninja-build
Requires:       gtk3-devel
Requires:       mesa-libGLU
# Removed dependency on vpython3 which isn't in Fedora repositories
ExclusiveArch:  x86_64 aarch64

%description
Flutter is Google's UI toolkit for building beautiful, natively compiled applications
for mobile, web, desktop, and embedded devices from a single codebase.

%prep
%setup -q -n flutter

# Patching to remove vpython3 dependency
# If flutter scripts expect vpython3, we need to modify them to use regular python3
find . -type f -exec sed -i 's|/usr/bin/vpython3|/usr/bin/python3|g' {} \;
find . -type f -exec sed -i 's|vpython3|python3|g' {} \;

# Pre-download some commonly used packages to avoid network access during build
./bin/flutter precache

%build
# Nothing to build specifically

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a * %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
ln -sf %{_datadir}/%{name}/bin/flutter %{buildroot}%{_bindir}/flutter

# Remove any remaining vpython references just to be safe
find %{buildroot} -type f -exec sed -i 's|/usr/bin/vpython3|/usr/bin/python3|g' {} \;
find %{buildroot} -type f -exec sed -i 's|vpython3|python3|g' {} \;

# Remove pre-compiled binaries for other platforms
rm -rf %{buildroot}%{_datadir}/%{name}/bin/cache/artifacts/engine/ios*
rm -rf %{buildroot}%{_datadir}/%{name}/bin/cache/artifacts/engine/android*
rm -rf %{buildroot}%{_datadir}/%{name}/bin/cache/artifacts/engine/darwin*
rm -rf %{buildroot}%{_datadir}/%{name}/bin/cache/artifacts/engine/windows*

%files
%license LICENSE
%{_bindir}/flutter
%{_datadir}/%{name}/
