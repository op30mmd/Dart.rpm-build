%global debug_package %{nil}
%global __strip /bin/true

Name:           dart
Version:        3.7.1
Release:        1%{?dist}
Summary:        Dart SDK - A programming language for web, servers, and mobile apps
License:        BSD
URL:            https://dart.dev/

# For x86_64
Source0:        https://storage.googleapis.com/dart-archive/channels/stable/release/%{version}/sdk/dartsdk-linux-x64-release.zip
# For aarch64
Source1:        https://storage.googleapis.com/dart-archive/channels/stable/release/%{version}/sdk/dartsdk-linux-arm64-release.zip

BuildRequires:  unzip
BuildRequires:  chrpath
ExclusiveArch:  x86_64 aarch64

%description
Dart is a class-based, single inheritance, object-oriented language
with C-style syntax. It offers compilation to JavaScript, interfaces,
mixins, abstract classes, reified generics, and optional typing.

%prep
%ifarch x86_64
%setup -q -n dart-sdk
%endif
%ifarch aarch64
%setup -q -n dart-sdk -b 1
%endif

%build
# Nothing to build, using precompiled binaries

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a bin include lib %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
ln -sf %{_datadir}/%{name}/bin/dart %{buildroot}%{_bindir}/dart
ln -sf %{_datadir}/%{name}/bin/dartaotruntime %{buildroot}%{_bindir}/dartaotruntime

# Remove rpath
find %{buildroot}%{_datadir}/%{name}/bin -type f -perm /0111 -exec chrpath -d {} \; || :

%files
%license LICENSE
%{_bindir}/dart
%{_bindir}/dartaotruntime
%{_datadir}/%{name}/
