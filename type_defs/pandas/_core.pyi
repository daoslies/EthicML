from typing import (
    Any,
    Tuple,
    List,
    Union,
    Callable,
    Dict,
    Iterator,
    Type,
    IO,
    Optional,
    overload,
    Sequence,
    Generic,
    TypeVar,
)
from pathlib import Path as _Path
import numpy as _np

_T = TypeVar('_T', str, int)

class Index(Generic[_T]):
    @property
    def values(self) -> _np.ndarray: ...
    def __getitem__(self, idx: int) -> _T: ...
    def __iter__(self) -> Iterator: ...
    def astype(self, dtype: Type) -> Index: ...
    def to_frame(self) -> DataFrame: ...

class Series:
    def min(self) -> float: ...
    def max(self) -> float: ...
    @property
    def shape(self) -> Tuple[int, ...]: ...
    def to_numpy(self) -> _np.ndarray: ...
    def unique(self) -> List[float]: ...
    def nunique(self) -> int: ...
    def __and__(self, other: Series) -> Series: ...
    def __eq__(self, other: object) -> Series: ...  # type: ignore
    @property
    def values(self) -> _np.ndarray: ...
    @overload
    def __getitem__(self, idx: int) -> float: ...
    @overload
    def __getitem__(self, idx: Union[List[str], Index[int], Series, slice]) -> Series: ...
    def value_counts(self) -> Series: ...
    def count(self) -> int: ...
    def __truediv__(self, other: object) -> Series: ...
    @property
    def index(self) -> Index[int]: ...
    def replace(self, to_replace: int, value: int, inplace: bool): ...

_ListLike = Union[_np.ndarray, Series, List, Dict[str, _np.ndarray]]

class DataFrame:
    def __init__(
        self,
        data: Optional[Union[_ListLike, DataFrame]] = ...,
        columns: Optional[Union[List[str], Index]] = ...,
        index: Optional[Union[_np.ndarray, Index]] = ...,
    ): ...
    @overload
    def __getitem__(self, idx: str) -> Series: ...
    @overload
    def __getitem__(self, idx: Union[List[str], Index]) -> DataFrame: ...
    @property
    def iloc(self) -> _iLocIndexer: ...
    @property
    def size(self) -> int: ...
    @property
    def shape(self) -> Tuple[int, ...]: ...
    @property
    def loc(self) -> _LocIndexer: ...
    @property
    def index(self) -> Index[int]: ...
    @property
    def columns(self) -> Index[str]: ...
    @columns.setter
    def columns(self, cols: Union[List[str], Index[str]]): ...
    def copy(self) -> DataFrame: ...
    @property
    def values(self) -> _np.ndarray: ...
    def __len__(self) -> int: ...
    def reset_index(self, drop: bool) -> DataFrame: ...
    def sample(self, frac: float, random_state: int, replace: bool = ...) -> DataFrame: ...
    def set_index(self, index: List[str]) -> DataFrame: ...
    def to_csv(self, filename: _Path, index: bool = ...) -> None: ...
    def to_feather(self, filename: _Path) -> None: ...
    def append(self, s: Dict[str, Any], ignore_index: bool = ...): ...
    def apply(self, f: Callable) -> DataFrame: ...
    def replace(self, a: float, b: float) -> DataFrame: ...
    def to_numpy(self) -> _np.ndarray: ...
    def rename(self, mapper: Callable, axis: str = ...) -> DataFrame: ...
    def query(self, expr: str) -> DataFrame: ...
    def head(self, n: int) -> DataFrame: ...
    def count(self) -> Series: ...

class _iLocIndexer:
    @overload
    def __getitem__(self, idx: int) -> Series: ...
    @overload
    def __getitem__(self, idx: Union[slice, Sequence[int], _np.ndarray[int]]) -> DataFrame: ...
    @overload
    def __setitem__(self, idx: int, value: Series): ...
    @overload
    def __setitem__(self, idx: Union[slice, Sequence[int], _np.ndarray[int]], value: DataFrame): ...

class _LocIndexer:
    def __getitem__(self, idx: Any) -> DataFrame: ...
    def __setitem__(self, idx: Any, value: Series): ...

def read_feather(p: Union[_Path, IO]) -> DataFrame: ...
def concat(
    dataframes: List[DataFrame],
    axis: str = ...,
    sort: Optional[bool] = ...,
    ignore_index: bool = ...,
) -> DataFrame: ...
def read_csv(p: _Path) -> DataFrame: ...
def isnull(df: Union[DataFrame, Series]) -> _np.ndarray: ...
