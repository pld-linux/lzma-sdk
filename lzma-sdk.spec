Summary:	LZMA Encoder/Decoder
Summary(pl.UTF-8):	Koder/Dekoder LZMA
Name:		lzma-sdk
Version:	19.00
%define	fver	%(echo %{version} | tr -d .)
Release:	1
License:	Public Domain
Group:		Applications/Archiving
Source0:	https://www.7-zip.org/a/lzma%{fver}.7z
# Source0-md5:	9d0411963b9d604a73833e1cc8289522
URL:		https://www.7-zip.org/sdk.html
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	p7zip
# does not need -libs, due apps being not linked with shared lib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZMA is an improved version of famous LZ77 compression algorithm. It
was improved in way of maximum increasing of compression ratio,
keeping high decompression speed and low memory requirements for 
decompressing.

LZMA features:
- compressing speed: ~2MB/s on 2 GHz CPU
- decompressing speed:
  - 20-30 MB/s on modern 2 GHz CPU
  - 1-2 MB/s on 200 MHz simple RISC CPU (ARM, MIPS, PowerPC)
- small memory requirements for decompressing: 16 kB + dictionary
  size
- small code size for decompressing: 5-8 kB

%description -l pl.UTF-8
LZMA to ulepszona wersja słynnego algorytmu kompresji LZ77. Został
poprawiony, aby maksymalnie zwiększyć stopień kompresji, utrzymując
wysoką szybkość i małe wymagania pamięciowe dekompresji.

Cechy LZMA:
- szybkość kompresowania: ~2MB/s na 2 GHz procesorze,
- szybkość dekompresowania:
  - 20-30 MB/s na współczesnym 2 GHz procesorze,
  - 1-2 MB/s na prostym procesorze RISC 200 MHz (ARM, MIPS, PowerPC)
- mała ilość pamięci potrzebna do dekompresowania: 16 kB + rozmiar
  słownika,
- mały rozmiar kodu dekompresującego: 5-8 kB

%package libs
Summary:	LZMA SDK shared library
Summary(pl.UTF-8):	Biblioteka współdzielona LZMA SDK
Group:		Libraries

%description libs
LZMA SDK shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona LZMA SDK.

%package devel
Summary:	Header file for LZMA SDK library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki LZMA SDK
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for LZMA SDK library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki LZMA SDK.

%package static
Summary:	LZMA SDK static library
Summary(pl.UTF-8):	Biblioteka statyczna LZMA SDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
LZMA SDK static library.

%description static -l pl.UTF-8
Biblioteka statyczna LZMA SDK.

%prep
%setup -q -c

%build
LIBFILES="Alloc LzFind LzmaDec LzmaEnc LzmaLib"
for f in $LIBFILES ; do
	libtool --tag CC --mode=compile %{__cc} -o ${f}.lo %{rpmcflags} %{rpmcppflags} -D_7ZIP_ST -c C/${f}.c
done
libtool --tag CC --mode=link %{__cc} -o liblzmasdk.la %{rpmldflags} %{rpmcflags} *.lo -rpath %{_libdir}

%{__make} -C C/Util/7z -f makefile.gcc \
	CXX="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -c" \
	LDFLAGS="%{rpmldflags}"

%{__make} -C C/Util/Lzma -f makefile.gcc  \
	CXX="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -D_7ZIP_ST -c" \
	LDFLAGS="%{rpmldflags}"

%{__make} -C CPP/7zip/Bundles/LzmaCon -f makefile.gcc \
	CXX="%{__cxx}" \
	CXX_C="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -D_7ZIP_ST -c" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/lzma-sdk,%{_libdir}}

libtool --mode=install install liblzmasdk.la $RPM_BUILD_ROOT%{_libdir}
# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblzmasdk.la

cp -p C/{7zTypes,LzmaLib}.h $RPM_BUILD_ROOT%{_includedir}/lzma-sdk

cp -p C/Util/7z/7zDec $RPM_BUILD_ROOT%{_bindir}
cp -p C/Util/Lzma/lzma $RPM_BUILD_ROOT%{_bindir}/lzma-c
cp -p CPP/7zip/Bundles/LzmaCon/lzma $RPM_BUILD_ROOT%{_bindir}/lzma-cpp

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DOC/{7zFormat,Methods,lzma,lzma-history,lzma-sdk,lzma-specification}.txt
%attr(755,root,root) %{_bindir}/7zDec
%attr(755,root,root) %{_bindir}/lzma-c
%attr(755,root,root) %{_bindir}/lzma-cpp

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblzmasdk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblzmasdk.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblzmasdk.so
%{_includedir}/lzma-sdk

%files static
%defattr(644,root,root,755)
%{_libdir}/liblzmasdk.a
