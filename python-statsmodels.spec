%define	module	statsmodels
%define name	python-%{module}
%define version 0.4.3
%define	rel	1
%if %mdkversion < 201100
%define release %mkrel %{rel}
%else
%define	release	%{rel}
%endif

Summary:	Statistical computations and models for use with SciPy
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://pypi.python.org/packages/source/s/%{module}/%{module}-%{version}.tar.gz
Patch0:		setup-lm-0.4.3.patch
Patch1:		build-doc-0.4.3.patch
License:	BSD
Group:		Development/Python
Url:		https://statsmodels.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	python-numpy >= 1.4.0
Requires:	python-scipy >= 0.7.0
Requires:	python-pandas >= 0.7.1
BuildRequires:	python-devel, python-setuptools
BuildRequires:	python-sphinx, python-matplotlib
BuildRequires:	python-numpy-devel >= 1.4.0
BuildRequires:	python-scipy >= 0.7.0
BuildRequires:	python-pandas >= 0.7.1
BuildRequires:	ipython

%description
Statsmodels is a Python module that allows users to explore data,
estimate statistical models, and perform statistical tests. An
extensive list of descriptive statistics, statistical tests, plotting
functions, and result statistics are available for different types of
data and each estimator. Researchers across fields may find that
statsmodels fully meets their needs for statistical computing and data
analysis in Python.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p0
%patch1 -p0

%build
%__python setup.py build 

%install
%__rm -rf %{buildroot}
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}

# Copy datasets into build directory tree to use when building docs:
pushd statsmodels
export PYTHONPATH=`ls -d ../build/lib* | head -1`
for f in `find . -name *.csv`; do \
cp --parents $f $PYTHONPATH/statsmodels/; \
done
popd

pushd docs
chmod u+x ../tools/*.py
make html
popd

find docs -name .buildinfo -exec rm -rf {} \;

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt COPYRIGHTS.txt LICENSE.txt README.txt examples/ docs/build/html
%py_platsitedir/scikits*
%py_platsitedir/statsmodels*

