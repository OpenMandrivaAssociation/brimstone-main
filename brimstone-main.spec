%define section         free
%define gcj_support     1

Name:           brimstone-main
Version:        0.1.20
Release:        %mkrel 0.0.5
Epoch:          0
Summary:        org.freecompany.brimstone
License:        MIT
Group:          Development/Java
URL:            https://www.freecompany.org/
# svn export https://svn.freecompany.org/public/brimstone/tags/brimstone-main-0.1.20 | yes t
# zip -9r brimstone-main-src-0.1.20.zip brimstone-main-0.1.20
Source0:        http://repository.freecompany.org/org/freecompany/brimstone/zips/brimstone-main-src-%{version}.zip
Source1:        brimstone-main-0.1.20-build.xml
Requires:       brimstone-core
Requires:       brimstone-module
Requires:       yacli
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  brimstone-cache
BuildRequires:  brimstone-core
BuildRequires:  brimstone-module
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
BuildRequires:  yacli
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.brimstone

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit brimstone-cache brimstone-core brimstone-module yacli)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} jar javadoc

%install
%{__rm} -rf %{buildroot}

# XXX: there's more to install in this package

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
