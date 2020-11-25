from typing import Any, Dict

import numpy as np
from pydantic.fields import Field

from scanspec.core import WithType


class Region(WithType):
    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        # Return a mask of which positions are in the region
        raise NotImplementedError(self)

    def __or__(self, other: "Region") -> "Region":
        if isinstance(other, Region):
            return UnionOf(self, other)
        else:
            return NotImplemented

    def __and__(self, other: "Region") -> "Region":
        if isinstance(other, Region):
            return IntersectionOf(self, other)
        else:
            return NotImplemented

    def __sub__(self, other: "Region") -> "Region":
        if isinstance(other, Region):
            return DifferenceOf(self, other)
        else:
            return NotImplemented

    def __xor__(self, other: "Region") -> "Region":
        if isinstance(other, Region):
            return SymmetricDifferenceOf(self, other)
        else:
            return NotImplemented


# Naming so we don't clash with typing.Union
class UnionOf(Region):
    left: Region
    right: Region

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        mask = self.left.mask(positions) | self.right.mask(positions)
        return mask


class IntersectionOf(Region):
    left: Region
    right: Region

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        mask = self.left.mask(positions) & self.right.mask(positions)
        return mask


class DifferenceOf(Region):
    left: Region
    right: Region

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        left_mask = self.left.mask(positions)
        # Subtract the right mask wherever the left mask is present
        mask = np.subtract(left_mask, self.right.mask(positions), where=left_mask)
        return mask


class SymmetricDifferenceOf(Region):
    left: Region
    right: Region

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        mask = self.left.mask(positions) ^ self.right.mask(positions)
        return mask


class Rectangle(Region):
    x_key: Any = Field(..., description="The key matching the x axis of the spec")
    y_key: Any = Field(..., description="The key matching the x axis of the spec")
    x_min: float = Field(..., description="Minimum inclusive x value in the region")
    y_min: float = Field(..., description="Minimum inclusive y value in the region")
    x_max: float = Field(..., description="Maximum inclusive x value in the region")
    y_max: float = Field(..., description="Maximum inclusive y value in the region")
    angle: float = Field(0, description="Clockwise rotation angle of the rectangle")

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        x = positions[self.x_key] - self.x_min
        y = positions[self.y_key] - self.y_min
        if self.angle != 0:
            # Rotate src positions by -angle
            phi = np.radians(-self.angle)
            rx = x * np.cos(phi) - y * np.sin(phi)
            ry = x * np.sin(phi) + y * np.cos(phi)
            x = rx
            y = ry
        mask_x = np.bitwise_and(x >= 0, x <= (self.x_max - self.x_min))
        mask_y = np.bitwise_and(y >= 0, y <= (self.y_max - self.y_min))
        return mask_x & mask_y


class Circle(Region):
    x_key: Any = Field(..., description="The key matching the x axis of the spec")
    y_key: Any = Field(..., description="The key matching the x axis of the spec")
    x_centre: float = Field(
        ..., description="Minimum inclusive x value in the region", alias="x_center"
    )
    y_centre: float = Field(
        ..., description="Minimum inclusive y value in the region", alias="y_center"
    )
    radius: float = Field(..., description="Radius of the circle")

    class Config:
        # Allow either centre or center
        allow_population_by_field_name = True

    def mask(self, positions: Dict[Any, np.ndarray]) -> np.ndarray:
        x = positions[self.x_key] - self.x_centre
        y = positions[self.y_key] - self.y_centre
        mask = x * x + y * y <= (self.radius * self.radius)
        return mask
