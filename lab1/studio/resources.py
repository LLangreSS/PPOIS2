from studio.exceptions import InvalidDataFormatError


class Resource:
    def __init__(self):
        self._is_busy: bool = False

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @is_busy.setter
    def is_busy(self, value: bool):
        if not isinstance(value, bool):
            raise InvalidDataFormatError("Status must be a boolean.")
        self._is_busy = value


class Camera(Resource):
    def __init__(self, model: str, resolution: str = "4K"):
        super().__init__()
        self._model = model
        self._resolution = resolution

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        if not value:
            raise InvalidDataFormatError("Camera model cannot be empty.")
        self._model = value

    def __str__(self) -> str:
        status = "[BUSY]" if self._is_busy else "[FREE]"
        return f"Camera: {self._model} ({self._resolution}) {status}"


class MovieSet(Resource):
    def __init__(self, location: str, is_indoor: bool):
        super().__init__()
        self._location = location
        self._is_indoor = is_indoor

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        if not value:
            raise InvalidDataFormatError("Location name cannot be empty.")
        self._location = value

    def __str__(self) -> str:
        env = "Indoor" if self._is_indoor else "Outdoor"
        status = "[BUSY]" if self._is_busy else "[FREE]"
        return f"Set: {self._location} ({env}) {status}"


class Montage:
    def __init__(self, software: str):
        self._software = software

    def apply_edits(self, title: str) -> str:
        return f"Editing '{title}' using {self._software}..."


class PostProduction:
    def __init__(self, department_name: str):
        self._department_name = department_name

    def finalize_movie(self, title: str) -> str:
        return f"VFX for '{title}' at {self._department_name}."
