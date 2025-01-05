import awkward as ak


class _Bes3EventReader:
    def __init__(self, file: list[str]) -> None: ...

    def get_entries(self) -> int: ...

    def get_available_fields(self) -> list[str]: ...

    def arrays(self,
               entry_start: int,
               entry_stop: int,
               field_names: list[str]) -> dict[str, ak.Array]: ...
