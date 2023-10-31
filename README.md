# Custom Datastructures for Fields with JAX
[![CodeFactor](https://www.codefactor.io/repository/github/jejjohnson/fieldx/badge)](https://www.codefactor.io/repository/github/jejjohnson/fieldx)
[![codecov](https://codecov.io/gh/jejjohnson/fieldx/branch/main/graph/badge.svg?token=YGPQQEAK91)](https://codecov.io/gh/jejjohnson/fieldx)

> This package takes inspiration from xarray datasets whereby we need access to the values of the field and the domain.



---
## Key Features

**Domains**.
This package has some simple domains like Cartesian. Later, we would like to include more complex domains like spherical
and cylindrical.

**Fields**.
This package has a custom datastructure which is a field which includes values and the domain. 

**Operators**. 
This package has simple operators that are useful for fields. They include constant operators and field operators.


---
## Installation

We can install it directly through pip

```bash
pip install git+https://github.com/jejjohnson/fieldx
```

We also use poetry for the development environment.

```bash
git clone https://github.com/jejjohnson/fieldx.git
cd fieldx
conda create -n fieldx python=3.11 poetry
poetry install
```



---
## References

**Software**

* [jaxdf](https://github.com/ucl-bug/jaxdf/tree/main) - Arbitrary Discretizations
* [diffrax (example)](https://docs.kidger.site/diffrax/examples/nonlinear_heat_pde/) - example of diffrax (and equinox) with an finite difference discretization