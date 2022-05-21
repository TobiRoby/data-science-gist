"""Data(frame) schemas."""
from pandera import Field, SchemaModel
from pandera.typing import Series


class StrictModel(SchemaModel):
    """Strict model schema: no differences from specified columns allowed."""

    class Config:
        """Schema configuration."""

        strict = True


class DataAdapterModel(StrictModel):
    """Data adapter model schema: coerce incoming data to expected."""

    class Config:
        """Schema configuration."""

        coerce = True


class IrisData(DataAdapterModel):
    """Iris data set."""

    sepal_length: Series[float] = Field(ge=0, le=10, description="length of sepal")
    sepal_width: Series[float] = Field(ge=0, le=10, description="width of sepal")
    petal_length: Series[float] = Field(ge=0, le=10, description="length of petal")
    petal_width: Series[float] = Field(ge=0, le=10, description="width of petal")
    species: Series[str] = Field(description="Iris species")
