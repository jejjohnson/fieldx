import typing as tp
import equinox as eqx
import jax.numpy as jnp
import numpy as np
# import jaxsw._src.domain.utils as d_utils
from fieldx._src.domain.utils import make_coords, make_grid_from_coords, make_grid_coords, create_meshgrid_coordinates
from jaxtyping import Array
from functools import reduce
from operator import mul


def check_inputs(x, name: str):
    if isinstance(x, float) or isinstance(x, int):
        return tuple([x])
    elif isinstance(x, list):
        return tuple(x)
    elif isinstance(x, tuple):
        return x
    elif isinstance(x, jnp.ndarray) or isinstance(x, np.ndarray):
        return tuple(map(lambda x: float(x), x))
    raise ValueError(f"Unexpected type for {name}, got {value}.")


class Domain(eqx.Module):
    """Domain class for a rectangular domain

    Attributes:
        size (Tuple[int]): The size of the domain
        xmin: (Iterable[float]): The min bounds for the input domain
        xmax: (Iterable[float]): The max bounds for the input domain
        coord (List[Array]): The coordinates of the domain
        grid (Array): A grid of the domain
        ndim (int): The number of dimenions of the domain
        size (Tuple[int]): The size of each dimenions of the domain
        cell_volume (float): The total volume of a grid cell
    """

    xmin: tp.Iterable[float] = eqx.static_field()
    xmax: tp.Iterable[float] = eqx.static_field()
    dx: tp.Iterable[float] = eqx.static_field()
    Nx: tp.Iterable[int] = eqx.static_field()
    Lx: tp.Iterable[float] = eqx.static_field()
    ndim: int = eqx.static_field()

    def __init__(
        self,
        xmin: tp.Union[float, tp.Iterable[float]],
        xmax: tp.Union[float, tp.Iterable[float]],
        dx: tp.Union[float, tp.Iterable[float]],
        Nx: tp.Union[int, tp.Iterable[int]],
        Lx: tp.Union[float, tp.Iterable[float]],
    ):
        xmin = check_inputs(xmin, name="xmin")
        xmax = check_inputs(xmax, name="xmax")
        dx = check_inputs(dx, name="dx")
        Nx = check_inputs(Nx, name="Nx")
        Lx = check_inputs(Lx, name="Lx")
        assert len(xmin) == len(xmax) == len(dx) == len(Nx) == len(Lx)
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.Nx = Nx
        self.Lx = Lx
        self.ndim = len(self.xmin)

    @property
    def coords_axis(self) -> tp.List:
        return list(map(make_coords, self.xmin, self.xmax, self.Nx))

    @property
    def grid_axis(self) -> Array:
        return make_grid_from_coords(self.coords_axis)

    @property
    def coords(self) -> Array:
        return jnp.asarray(make_grid_coords(self.coords_axis))

    @property
    def cell_volume(self) -> float:
        return reduce(mul, self.dx)

    def __getitem__(self, values):
        if isinstance(values, (jnp.ndarray, np.ndarray, tuple)):
            values = list(values)
        elif isinstance(values, slice):
            values = list([values])

        try:
            iter(values)
        except TypeError:
            values = list(values)

        if Ellipsis in values:
            raise ValueError(f"Ellipsis not allowed. MUST be explicit.")

        msg = f"Incompatible slice. MUST be explicit"
        assert len(values) == len(self.coords_axis), msg

        # get sliced coordinates
        # sliced_coords = [jax.lax.slice(idx, [islice.start], [slice.stop], [islice.step]) for idx, islice in zip(self.coords_axis, values)]
        sliced_coords = [idx[islice] for idx, islice in zip(self.coords_axis, values)]

        # change Nx
        Nx = list(map(lambda x: len(x), sliced_coords))

        # change Lx
        fn = lambda Lx, Nx, Ny: Lx * (Ny / Nx)
        Lx = list(map(fn, self.Lx, self.Nx, Nx))

        # change xmin, xmax
        xmin = tuple(map(lambda x: float(x[0]), sliced_coords))
        xmax = tuple(map(lambda x: float(x[-1]), sliced_coords))

        return Domain(xmin=xmin, xmax=xmax, Lx=Lx, Nx=Nx, dx=self.dx)

    def __mul__(self, other):
        fn = lambda x, y: x + y

        xmin = fn(self.xmin, other.xmin)
        xmax = fn(self.xmax, other.xmax)
        dx = fn(self.dx, other.dx)
        Nx = fn(self.Nx, other.Nx)
        Lx = fn(self.Lx, other.Lx)
        return Domain(xmin=xmin, xmax=xmax, dx=dx, Nx=Nx, Lx=Lx)

    def __rmult__(self, other):
        fn = lambda x, y: y + x

        xmin = fn(self.xmin, other.xmin)
        xmax = fn(self.xmax, other.xmax)
        dx = fn(self.dx, other.dx)
        Nx = fn(self.Nx, other.Nx)
        Lx = fn(self.Lx, other.Lx)
        return Domain(xmin=xmin, xmax=xmax, dx=dx, Nx=Nx, Lx=Lx)
