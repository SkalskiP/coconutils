from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import List, Optional, Union


@dataclass(frozen=True)
class COCOInfo(DataClassJsonMixin):
    url: Optional[str] = None
    version: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    date_created: Optional[str] = None
    contributor: Optional[str] = None
    data_created: Optional[str] = None
    data_modified: Optional[str] = None
    license: Optional[str] = None
    license_url: Optional[str] = None


@dataclass(frozen=True)
class COCOImage(DataClassJsonMixin):
    id: int
    width: int
    height: int
    file_name: str
    coco_url: Optional[str] = None
    flickr_url: Optional[str] = None
    date_captured: Optional[str] = None


@dataclass(frozen=True)
class COCOAnnotation(DataClassJsonMixin):
    id: int
    image_id: int
    category_id: int
    segmentation: Optional[List[List[float]]] = None
    area: Optional[float] = None
    bbox: Optional[List[float]] = None
    iscrowd: Optional[int] = None


@dataclass(frozen=True)
class COCOCategory(DataClassJsonMixin):
    id: int
    name: str
    supercategory: Optional[str] = None


@dataclass(frozen=True)
class COCO(DataClassJsonMixin):
    info: COCOInfo
    images: List[COCOImage]
    annotations: List[COCOAnnotation]
    categories: List[COCOCategory]