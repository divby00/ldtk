# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = ldtk_json_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, List, Any, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


class EditorDisplayMode(Enum):
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`
    """
    ENTITY_TILE = "EntityTile"
    HIDDEN = "Hidden"
    NAME_AND_VALUE = "NameAndValue"
    POINTS = "Points"
    POINT_PATH = "PointPath"
    POINT_PATH_LOOP = "PointPathLoop"
    POINT_STAR = "PointStar"
    RADIUS_GRID = "RadiusGrid"
    RADIUS_PX = "RadiusPx"
    VALUE_ONLY = "ValueOnly"


class EditorDisplayPos(Enum):
    """Possible values: `Above`, `Center`, `Beneath`"""
    ABOVE = "Above"
    BENEATH = "Beneath"
    CENTER = "Center"


class TextLangageMode(Enum):
    LANG_C = "LangC"
    LANG_HAXE = "LangHaxe"
    LANG_JS = "LangJS"
    LANG_JSON = "LangJson"
    LANG_LUA = "LangLua"
    LANG_MARKDOWN = "LangMarkdown"
    LANG_PYTHON = "LangPython"
    LANG_RUBY = "LangRuby"
    LANG_XML = "LangXml"


class FieldDefinition:
    """This section is mostly only intended for the LDtk editor app itself. You can safely
    ignore it.
    """
    """Human readable value type (eg. `Int`, `Float`, `Point`, etc.). If the field is an array,
    this field will look like `Array<...>` (eg. `Array<Int>`, `Array<Point>` etc.)
    """
    type: str
    """Optional list of accepted file extensions for FilePath value type. Includes the dot:
    `.ext`
    """
    accept_file_types: Optional[List[str]]
    """Array max length"""
    array_max_length: Optional[int]
    """Array min length"""
    array_min_length: Optional[int]
    """TRUE if the value can be null. For arrays, TRUE means it can contain null values
    (exception: array of Points can't have null values).
    """
    can_be_null: bool
    """Default value if selected value is null or invalid."""
    default_override: Any
    editor_always_show: bool
    editor_cut_long_values: bool
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`
    """
    editor_display_mode: EditorDisplayMode
    """Possible values: `Above`, `Center`, `Beneath`"""
    editor_display_pos: EditorDisplayPos
    """Unique String identifier"""
    identifier: str
    """TRUE if the value is an array of multiple values"""
    is_array: bool
    """Max limit for value, if applicable"""
    max: Optional[float]
    """Min limit for value, if applicable"""
    min: Optional[float]
    """Optional regular expression that needs to be matched to accept values. Expected format:
    `/some_reg_ex/g`, with optional "i" flag.
    """
    regex: Optional[str]
    """Possible values: &lt;`null`&gt;, `LangPython`, `LangRuby`, `LangJS`, `LangLua`, `LangC`,
    `LangHaxe`, `LangMarkdown`, `LangJson`, `LangXml`
    """
    text_langage_mode: Optional[TextLangageMode]
    """Internal type enum"""
    field_definition_type: Any
    """Unique Int identifier"""
    uid: int

    def __init__(self, type: str, accept_file_types: Optional[List[str]], array_max_length: Optional[int], array_min_length: Optional[int], can_be_null: bool, default_override: Any, editor_always_show: bool, editor_cut_long_values: bool, editor_display_mode: EditorDisplayMode, editor_display_pos: EditorDisplayPos, identifier: str, is_array: bool, max: Optional[float], min: Optional[float], regex: Optional[str], text_langage_mode: Optional[TextLangageMode], field_definition_type: Any, uid: int) -> None:
        self.type = type
        self.accept_file_types = accept_file_types
        self.array_max_length = array_max_length
        self.array_min_length = array_min_length
        self.can_be_null = can_be_null
        self.default_override = default_override
        self.editor_always_show = editor_always_show
        self.editor_cut_long_values = editor_cut_long_values
        self.editor_display_mode = editor_display_mode
        self.editor_display_pos = editor_display_pos
        self.identifier = identifier
        self.is_array = is_array
        self.max = max
        self.min = min
        self.regex = regex
        self.text_langage_mode = text_langage_mode
        self.field_definition_type = field_definition_type
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'FieldDefinition':
        assert isinstance(obj, dict)
        type = from_str(obj.get("__type"))
        accept_file_types = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("acceptFileTypes"))
        array_max_length = from_union([from_none, from_int], obj.get("arrayMaxLength"))
        array_min_length = from_union([from_none, from_int], obj.get("arrayMinLength"))
        can_be_null = from_bool(obj.get("canBeNull"))
        default_override = obj.get("defaultOverride")
        editor_always_show = from_bool(obj.get("editorAlwaysShow"))
        editor_cut_long_values = from_bool(obj.get("editorCutLongValues"))
        editor_display_mode = EditorDisplayMode(obj.get("editorDisplayMode"))
        editor_display_pos = EditorDisplayPos(obj.get("editorDisplayPos"))
        identifier = from_str(obj.get("identifier"))
        is_array = from_bool(obj.get("isArray"))
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        regex = from_union([from_none, from_str], obj.get("regex"))
        text_langage_mode = from_union([from_none, TextLangageMode], obj.get("textLangageMode"))
        field_definition_type = obj.get("type")
        uid = from_int(obj.get("uid"))
        return FieldDefinition(type, accept_file_types, array_max_length, array_min_length, can_be_null, default_override, editor_always_show, editor_cut_long_values, editor_display_mode, editor_display_pos, identifier, is_array, max, min, regex, text_langage_mode, field_definition_type, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_str(self.type)
        result["acceptFileTypes"] = from_union([from_none, lambda x: from_list(from_str, x)], self.accept_file_types)
        result["arrayMaxLength"] = from_union([from_none, from_int], self.array_max_length)
        result["arrayMinLength"] = from_union([from_none, from_int], self.array_min_length)
        result["canBeNull"] = from_bool(self.can_be_null)
        result["defaultOverride"] = self.default_override
        result["editorAlwaysShow"] = from_bool(self.editor_always_show)
        result["editorCutLongValues"] = from_bool(self.editor_cut_long_values)
        result["editorDisplayMode"] = to_enum(EditorDisplayMode, self.editor_display_mode)
        result["editorDisplayPos"] = to_enum(EditorDisplayPos, self.editor_display_pos)
        result["identifier"] = from_str(self.identifier)
        result["isArray"] = from_bool(self.is_array)
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["regex"] = from_union([from_none, from_str], self.regex)
        result["textLangageMode"] = from_union([from_none, lambda x: to_enum(TextLangageMode, x)], self.text_langage_mode)
        result["type"] = self.field_definition_type
        result["uid"] = from_int(self.uid)
        return result


class LimitBehavior(Enum):
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""
    DISCARD_OLD_ONES = "DiscardOldOnes"
    MOVE_LAST_ONE = "MoveLastOne"
    PREVENT_ADDING = "PreventAdding"


class LimitScope(Enum):
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """
    PER_LAYER = "PerLayer"
    PER_LEVEL = "PerLevel"
    PER_WORLD = "PerWorld"


class RenderMode(Enum):
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""
    CROSS = "Cross"
    ELLIPSE = "Ellipse"
    RECTANGLE = "Rectangle"
    TILE = "Tile"


class TileRenderMode(Enum):
    """Possible values: `Cover`, `FitInside`, `Repeat`, `Stretch`"""
    COVER = "Cover"
    FIT_INSIDE = "FitInside"
    REPEAT = "Repeat"
    STRETCH = "Stretch"


class EntityDefinition:
    """Base entity color"""
    color: str
    """Array of field definitions"""
    field_defs: List[FieldDefinition]
    fill_opacity: float
    """Pixel height"""
    height: int
    hollow: bool
    """Unique String identifier"""
    identifier: str
    """Only applies to entities resizable on both X/Y. If TRUE, the entity instance width/height
    will keep the same aspect ratio as the definition.
    """
    keep_aspect_ratio: bool
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""
    limit_behavior: LimitBehavior
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """
    limit_scope: LimitScope
    line_opacity: float
    """Max instances count"""
    max_count: int
    """Pivot X coordinate (from 0 to 1.0)"""
    pivot_x: float
    """Pivot Y coordinate (from 0 to 1.0)"""
    pivot_y: float
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""
    render_mode: RenderMode
    """If TRUE, the entity instances will be resizable horizontally"""
    resizable_x: bool
    """If TRUE, the entity instances will be resizable vertically"""
    resizable_y: bool
    """Display entity name in editor"""
    show_name: bool
    """An array of strings that classifies this entity"""
    tags: List[str]
    """Tile ID used for optional tile display"""
    tile_id: Optional[int]
    """Possible values: `Cover`, `FitInside`, `Repeat`, `Stretch`"""
    tile_render_mode: TileRenderMode
    """Tileset ID used for optional tile display"""
    tileset_id: Optional[int]
    """Unique Int identifier"""
    uid: int
    """Pixel width"""
    width: int

    def __init__(self, color: str, field_defs: List[FieldDefinition], fill_opacity: float, height: int, hollow: bool, identifier: str, keep_aspect_ratio: bool, limit_behavior: LimitBehavior, limit_scope: LimitScope, line_opacity: float, max_count: int, pivot_x: float, pivot_y: float, render_mode: RenderMode, resizable_x: bool, resizable_y: bool, show_name: bool, tags: List[str], tile_id: Optional[int], tile_render_mode: TileRenderMode, tileset_id: Optional[int], uid: int, width: int) -> None:
        self.color = color
        self.field_defs = field_defs
        self.fill_opacity = fill_opacity
        self.height = height
        self.hollow = hollow
        self.identifier = identifier
        self.keep_aspect_ratio = keep_aspect_ratio
        self.limit_behavior = limit_behavior
        self.limit_scope = limit_scope
        self.line_opacity = line_opacity
        self.max_count = max_count
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.render_mode = render_mode
        self.resizable_x = resizable_x
        self.resizable_y = resizable_y
        self.show_name = show_name
        self.tags = tags
        self.tile_id = tile_id
        self.tile_render_mode = tile_render_mode
        self.tileset_id = tileset_id
        self.uid = uid
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'EntityDefinition':
        assert isinstance(obj, dict)
        color = from_str(obj.get("color"))
        field_defs = from_list(FieldDefinition.from_dict, obj.get("fieldDefs"))
        fill_opacity = from_float(obj.get("fillOpacity"))
        height = from_int(obj.get("height"))
        hollow = from_bool(obj.get("hollow"))
        identifier = from_str(obj.get("identifier"))
        keep_aspect_ratio = from_bool(obj.get("keepAspectRatio"))
        limit_behavior = LimitBehavior(obj.get("limitBehavior"))
        limit_scope = LimitScope(obj.get("limitScope"))
        line_opacity = from_float(obj.get("lineOpacity"))
        max_count = from_int(obj.get("maxCount"))
        pivot_x = from_float(obj.get("pivotX"))
        pivot_y = from_float(obj.get("pivotY"))
        render_mode = RenderMode(obj.get("renderMode"))
        resizable_x = from_bool(obj.get("resizableX"))
        resizable_y = from_bool(obj.get("resizableY"))
        show_name = from_bool(obj.get("showName"))
        tags = from_list(from_str, obj.get("tags"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        tile_render_mode = TileRenderMode(obj.get("tileRenderMode"))
        tileset_id = from_union([from_none, from_int], obj.get("tilesetId"))
        uid = from_int(obj.get("uid"))
        width = from_int(obj.get("width"))
        return EntityDefinition(color, field_defs, fill_opacity, height, hollow, identifier, keep_aspect_ratio, limit_behavior, limit_scope, line_opacity, max_count, pivot_x, pivot_y, render_mode, resizable_x, resizable_y, show_name, tags, tile_id, tile_render_mode, tileset_id, uid, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_str(self.color)
        result["fieldDefs"] = from_list(lambda x: to_class(FieldDefinition, x), self.field_defs)
        result["fillOpacity"] = to_float(self.fill_opacity)
        result["height"] = from_int(self.height)
        result["hollow"] = from_bool(self.hollow)
        result["identifier"] = from_str(self.identifier)
        result["keepAspectRatio"] = from_bool(self.keep_aspect_ratio)
        result["limitBehavior"] = to_enum(LimitBehavior, self.limit_behavior)
        result["limitScope"] = to_enum(LimitScope, self.limit_scope)
        result["lineOpacity"] = to_float(self.line_opacity)
        result["maxCount"] = from_int(self.max_count)
        result["pivotX"] = to_float(self.pivot_x)
        result["pivotY"] = to_float(self.pivot_y)
        result["renderMode"] = to_enum(RenderMode, self.render_mode)
        result["resizableX"] = from_bool(self.resizable_x)
        result["resizableY"] = from_bool(self.resizable_y)
        result["showName"] = from_bool(self.show_name)
        result["tags"] = from_list(from_str, self.tags)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        result["tileRenderMode"] = to_enum(TileRenderMode, self.tile_render_mode)
        result["tilesetId"] = from_union([from_none, from_int], self.tileset_id)
        result["uid"] = from_int(self.uid)
        result["width"] = from_int(self.width)
        return result


class EnumValueDefinition:
    """An array of 4 Int values that refers to the tile in the tileset image: `[ x, y, width,
    height ]`
    """
    tile_src_rect: Optional[List[int]]
    """Optional color"""
    color: int
    """Enum value"""
    id: str
    """The optional ID of the tile"""
    tile_id: Optional[int]

    def __init__(self, tile_src_rect: Optional[List[int]], color: int, id: str, tile_id: Optional[int]) -> None:
        self.tile_src_rect = tile_src_rect
        self.color = color
        self.id = id
        self.tile_id = tile_id

    @staticmethod
    def from_dict(obj: Any) -> 'EnumValueDefinition':
        assert isinstance(obj, dict)
        tile_src_rect = from_union([from_none, lambda x: from_list(from_int, x)], obj.get("__tileSrcRect"))
        color = from_int(obj.get("color"))
        id = from_str(obj.get("id"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        return EnumValueDefinition(tile_src_rect, color, id, tile_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__tileSrcRect"] = from_union([from_none, lambda x: from_list(from_int, x)], self.tile_src_rect)
        result["color"] = from_int(self.color)
        result["id"] = from_str(self.id)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        return result


class EnumDefinition:
    external_file_checksum: Optional[str]
    """Relative path to the external file providing this Enum"""
    external_rel_path: Optional[str]
    """Tileset UID if provided"""
    icon_tileset_uid: Optional[int]
    """Unique String identifier"""
    identifier: str
    """Unique Int identifier"""
    uid: int
    """All possible enum values, with their optional Tile infos."""
    values: List[EnumValueDefinition]

    def __init__(self, external_file_checksum: Optional[str], external_rel_path: Optional[str], icon_tileset_uid: Optional[int], identifier: str, uid: int, values: List[EnumValueDefinition]) -> None:
        self.external_file_checksum = external_file_checksum
        self.external_rel_path = external_rel_path
        self.icon_tileset_uid = icon_tileset_uid
        self.identifier = identifier
        self.uid = uid
        self.values = values

    @staticmethod
    def from_dict(obj: Any) -> 'EnumDefinition':
        assert isinstance(obj, dict)
        external_file_checksum = from_union([from_none, from_str], obj.get("externalFileChecksum"))
        external_rel_path = from_union([from_none, from_str], obj.get("externalRelPath"))
        icon_tileset_uid = from_union([from_none, from_int], obj.get("iconTilesetUid"))
        identifier = from_str(obj.get("identifier"))
        uid = from_int(obj.get("uid"))
        values = from_list(EnumValueDefinition.from_dict, obj.get("values"))
        return EnumDefinition(external_file_checksum, external_rel_path, icon_tileset_uid, identifier, uid, values)

    def to_dict(self) -> dict:
        result: dict = {}
        result["externalFileChecksum"] = from_union([from_none, from_str], self.external_file_checksum)
        result["externalRelPath"] = from_union([from_none, from_str], self.external_rel_path)
        result["iconTilesetUid"] = from_union([from_none, from_int], self.icon_tileset_uid)
        result["identifier"] = from_str(self.identifier)
        result["uid"] = from_int(self.uid)
        result["values"] = from_list(lambda x: to_class(EnumValueDefinition, x), self.values)
        return result


class Checker(Enum):
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""
    HORIZONTAL = "Horizontal"
    NONE = "None"
    VERTICAL = "Vertical"


class TileMode(Enum):
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""
    SINGLE = "Single"
    STAMP = "Stamp"


class AutoLayerRuleDefinition:
    """This complex section isn't meant to be used by game devs at all, as these rules are
    completely resolved internally by the editor before any saving. You should just ignore
    this part.
    """
    """If FALSE, the rule effect isn't applied, and no tiles are generated."""
    active: bool
    """When TRUE, the rule will prevent other rules to be applied in the same cell if it matches
    (TRUE by default).
    """
    break_on_match: bool
    """Chances for this rule to be applied (0 to 1)"""
    chance: float
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""
    checker: Checker
    """If TRUE, allow rule to be matched by flipping its pattern horizontally"""
    flip_x: bool
    """If TRUE, allow rule to be matched by flipping its pattern vertically"""
    flip_y: bool
    """Default IntGrid value when checking cells outside of level bounds"""
    out_of_bounds_value: Optional[int]
    """Rule pattern (size x size)"""
    pattern: List[int]
    """If TRUE, enable Perlin filtering to only apply rule on specific random area"""
    perlin_active: bool
    perlin_octaves: float
    perlin_scale: float
    perlin_seed: float
    """X pivot of a tile stamp (0-1)"""
    pivot_x: float
    """Y pivot of a tile stamp (0-1)"""
    pivot_y: float
    """Pattern width & height. Should only be 1,3,5 or 7."""
    size: int
    """Array of all the tile IDs. They are used randomly or as stamps, based on `tileMode` value."""
    tile_ids: List[int]
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""
    tile_mode: TileMode
    """Unique Int identifier"""
    uid: int
    """X cell coord modulo"""
    x_modulo: int
    """Y cell coord modulo"""
    y_modulo: int

    def __init__(self, active: bool, break_on_match: bool, chance: float, checker: Checker, flip_x: bool, flip_y: bool, out_of_bounds_value: Optional[int], pattern: List[int], perlin_active: bool, perlin_octaves: float, perlin_scale: float, perlin_seed: float, pivot_x: float, pivot_y: float, size: int, tile_ids: List[int], tile_mode: TileMode, uid: int, x_modulo: int, y_modulo: int) -> None:
        self.active = active
        self.break_on_match = break_on_match
        self.chance = chance
        self.checker = checker
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.out_of_bounds_value = out_of_bounds_value
        self.pattern = pattern
        self.perlin_active = perlin_active
        self.perlin_octaves = perlin_octaves
        self.perlin_scale = perlin_scale
        self.perlin_seed = perlin_seed
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.size = size
        self.tile_ids = tile_ids
        self.tile_mode = tile_mode
        self.uid = uid
        self.x_modulo = x_modulo
        self.y_modulo = y_modulo

    @staticmethod
    def from_dict(obj: Any) -> 'AutoLayerRuleDefinition':
        assert isinstance(obj, dict)
        active = from_bool(obj.get("active"))
        break_on_match = from_bool(obj.get("breakOnMatch"))
        chance = from_float(obj.get("chance"))
        checker = Checker(obj.get("checker"))
        flip_x = from_bool(obj.get("flipX"))
        flip_y = from_bool(obj.get("flipY"))
        out_of_bounds_value = from_union([from_none, from_int], obj.get("outOfBoundsValue"))
        pattern = from_list(from_int, obj.get("pattern"))
        perlin_active = from_bool(obj.get("perlinActive"))
        perlin_octaves = from_float(obj.get("perlinOctaves"))
        perlin_scale = from_float(obj.get("perlinScale"))
        perlin_seed = from_float(obj.get("perlinSeed"))
        pivot_x = from_float(obj.get("pivotX"))
        pivot_y = from_float(obj.get("pivotY"))
        size = from_int(obj.get("size"))
        tile_ids = from_list(from_int, obj.get("tileIds"))
        tile_mode = TileMode(obj.get("tileMode"))
        uid = from_int(obj.get("uid"))
        x_modulo = from_int(obj.get("xModulo"))
        y_modulo = from_int(obj.get("yModulo"))
        return AutoLayerRuleDefinition(active, break_on_match, chance, checker, flip_x, flip_y, out_of_bounds_value, pattern, perlin_active, perlin_octaves, perlin_scale, perlin_seed, pivot_x, pivot_y, size, tile_ids, tile_mode, uid, x_modulo, y_modulo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_bool(self.active)
        result["breakOnMatch"] = from_bool(self.break_on_match)
        result["chance"] = to_float(self.chance)
        result["checker"] = to_enum(Checker, self.checker)
        result["flipX"] = from_bool(self.flip_x)
        result["flipY"] = from_bool(self.flip_y)
        result["outOfBoundsValue"] = from_union([from_none, from_int], self.out_of_bounds_value)
        result["pattern"] = from_list(from_int, self.pattern)
        result["perlinActive"] = from_bool(self.perlin_active)
        result["perlinOctaves"] = to_float(self.perlin_octaves)
        result["perlinScale"] = to_float(self.perlin_scale)
        result["perlinSeed"] = to_float(self.perlin_seed)
        result["pivotX"] = to_float(self.pivot_x)
        result["pivotY"] = to_float(self.pivot_y)
        result["size"] = from_int(self.size)
        result["tileIds"] = from_list(from_int, self.tile_ids)
        result["tileMode"] = to_enum(TileMode, self.tile_mode)
        result["uid"] = from_int(self.uid)
        result["xModulo"] = from_int(self.x_modulo)
        result["yModulo"] = from_int(self.y_modulo)
        return result


class AutoLayerRuleGroup:
    active: bool
    collapsed: bool
    is_optional: bool
    name: str
    rules: List[AutoLayerRuleDefinition]
    uid: int

    def __init__(self, active: bool, collapsed: bool, is_optional: bool, name: str, rules: List[AutoLayerRuleDefinition], uid: int) -> None:
        self.active = active
        self.collapsed = collapsed
        self.is_optional = is_optional
        self.name = name
        self.rules = rules
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'AutoLayerRuleGroup':
        assert isinstance(obj, dict)
        active = from_bool(obj.get("active"))
        collapsed = from_bool(obj.get("collapsed"))
        is_optional = from_bool(obj.get("isOptional"))
        name = from_str(obj.get("name"))
        rules = from_list(AutoLayerRuleDefinition.from_dict, obj.get("rules"))
        uid = from_int(obj.get("uid"))
        return AutoLayerRuleGroup(active, collapsed, is_optional, name, rules, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_bool(self.active)
        result["collapsed"] = from_bool(self.collapsed)
        result["isOptional"] = from_bool(self.is_optional)
        result["name"] = from_str(self.name)
        result["rules"] = from_list(lambda x: to_class(AutoLayerRuleDefinition, x), self.rules)
        result["uid"] = from_int(self.uid)
        return result


class IntGridValueDefinition:
    """IntGrid value definition"""
    color: str
    """Unique String identifier"""
    identifier: Optional[str]
    """The IntGrid value itself"""
    value: int

    def __init__(self, color: str, identifier: Optional[str], value: int) -> None:
        self.color = color
        self.identifier = identifier
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'IntGridValueDefinition':
        assert isinstance(obj, dict)
        color = from_str(obj.get("color"))
        identifier = from_union([from_none, from_str], obj.get("identifier"))
        value = from_int(obj.get("value"))
        return IntGridValueDefinition(color, identifier, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_str(self.color)
        result["identifier"] = from_union([from_none, from_str], self.identifier)
        result["value"] = from_int(self.value)
        return result


class TypeEnum(Enum):
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """
    AUTO_LAYER = "AutoLayer"
    ENTITIES = "Entities"
    INT_GRID = "IntGrid"
    TILES = "Tiles"


class LayerDefinition:
    """Type of the layer (*IntGrid, Entities, Tiles or AutoLayer*)"""
    type: str
    """Contains all the auto-layer rule definitions."""
    auto_rule_groups: List[AutoLayerRuleGroup]
    auto_source_layer_def_uid: Optional[int]
    """Reference to the Tileset UID being used by this auto-layer rules. WARNING: some layer
    *instances* might use a different tileset. So most of the time, you should probably use
    the `__tilesetDefUid` value from layer instances.
    """
    auto_tileset_def_uid: Optional[int]
    """Opacity of the layer (0 to 1.0)"""
    display_opacity: float
    """An array of tags to forbid some Entities in this layer"""
    excluded_tags: List[str]
    """Width and height of the grid in pixels"""
    grid_size: int
    """Unique String identifier"""
    identifier: str
    """An array that defines extra optional info for each IntGrid value. The array is sorted
    using value (ascending).
    """
    int_grid_values: List[IntGridValueDefinition]
    """X offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_x: int
    """Y offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_y: int
    """An array of tags to filter Entities that can be added to this layer"""
    required_tags: List[str]
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_x: float
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_y: float
    """Reference to the Tileset UID being used by this Tile layer. WARNING: some layer
    *instances* might use a different tileset. So most of the time, you should probably use
    the `__tilesetDefUid` value from layer instances.
    """
    tileset_def_uid: Optional[int]
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """
    layer_definition_type: TypeEnum
    """Unique Int identifier"""
    uid: int

    def __init__(self, type: str, auto_rule_groups: List[AutoLayerRuleGroup], auto_source_layer_def_uid: Optional[int], auto_tileset_def_uid: Optional[int], display_opacity: float, excluded_tags: List[str], grid_size: int, identifier: str, int_grid_values: List[IntGridValueDefinition], px_offset_x: int, px_offset_y: int, required_tags: List[str], tile_pivot_x: float, tile_pivot_y: float, tileset_def_uid: Optional[int], layer_definition_type: TypeEnum, uid: int) -> None:
        self.type = type
        self.auto_rule_groups = auto_rule_groups
        self.auto_source_layer_def_uid = auto_source_layer_def_uid
        self.auto_tileset_def_uid = auto_tileset_def_uid
        self.display_opacity = display_opacity
        self.excluded_tags = excluded_tags
        self.grid_size = grid_size
        self.identifier = identifier
        self.int_grid_values = int_grid_values
        self.px_offset_x = px_offset_x
        self.px_offset_y = px_offset_y
        self.required_tags = required_tags
        self.tile_pivot_x = tile_pivot_x
        self.tile_pivot_y = tile_pivot_y
        self.tileset_def_uid = tileset_def_uid
        self.layer_definition_type = layer_definition_type
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'LayerDefinition':
        assert isinstance(obj, dict)
        type = from_str(obj.get("__type"))
        auto_rule_groups = from_list(AutoLayerRuleGroup.from_dict, obj.get("autoRuleGroups"))
        auto_source_layer_def_uid = from_union([from_none, from_int], obj.get("autoSourceLayerDefUid"))
        auto_tileset_def_uid = from_union([from_none, from_int], obj.get("autoTilesetDefUid"))
        display_opacity = from_float(obj.get("displayOpacity"))
        excluded_tags = from_list(from_str, obj.get("excludedTags"))
        grid_size = from_int(obj.get("gridSize"))
        identifier = from_str(obj.get("identifier"))
        int_grid_values = from_list(IntGridValueDefinition.from_dict, obj.get("intGridValues"))
        px_offset_x = from_int(obj.get("pxOffsetX"))
        px_offset_y = from_int(obj.get("pxOffsetY"))
        required_tags = from_list(from_str, obj.get("requiredTags"))
        tile_pivot_x = from_float(obj.get("tilePivotX"))
        tile_pivot_y = from_float(obj.get("tilePivotY"))
        tileset_def_uid = from_union([from_none, from_int], obj.get("tilesetDefUid"))
        layer_definition_type = TypeEnum(obj.get("type"))
        uid = from_int(obj.get("uid"))
        return LayerDefinition(type, auto_rule_groups, auto_source_layer_def_uid, auto_tileset_def_uid, display_opacity, excluded_tags, grid_size, identifier, int_grid_values, px_offset_x, px_offset_y, required_tags, tile_pivot_x, tile_pivot_y, tileset_def_uid, layer_definition_type, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_str(self.type)
        result["autoRuleGroups"] = from_list(lambda x: to_class(AutoLayerRuleGroup, x), self.auto_rule_groups)
        result["autoSourceLayerDefUid"] = from_union([from_none, from_int], self.auto_source_layer_def_uid)
        result["autoTilesetDefUid"] = from_union([from_none, from_int], self.auto_tileset_def_uid)
        result["displayOpacity"] = to_float(self.display_opacity)
        result["excludedTags"] = from_list(from_str, self.excluded_tags)
        result["gridSize"] = from_int(self.grid_size)
        result["identifier"] = from_str(self.identifier)
        result["intGridValues"] = from_list(lambda x: to_class(IntGridValueDefinition, x), self.int_grid_values)
        result["pxOffsetX"] = from_int(self.px_offset_x)
        result["pxOffsetY"] = from_int(self.px_offset_y)
        result["requiredTags"] = from_list(from_str, self.required_tags)
        result["tilePivotX"] = to_float(self.tile_pivot_x)
        result["tilePivotY"] = to_float(self.tile_pivot_y)
        result["tilesetDefUid"] = from_union([from_none, from_int], self.tileset_def_uid)
        result["type"] = to_enum(TypeEnum, self.layer_definition_type)
        result["uid"] = from_int(self.uid)
        return result


class TilesetDefinition:
    """The `Tileset` definition is the most important part among project definitions. It
    contains some extra informations about each integrated tileset. If you only had to parse
    one definition section, that would be the one.
    """
    """Grid-based height"""
    c_hei: int
    """Grid-based width"""
    c_wid: int
    """The following data is used internally for various optimizations. It's always synced with
    source image changes.
    """
    cached_pixel_data: Optional[Dict[str, Any]]
    """An array of custom tile metadata"""
    custom_data: List[Dict[str, Any]]
    """Tileset tags using Enum values specified by `tagsSourceEnumId`. This array contains 1
    element per Enum value, which contains an array of all Tile IDs that are tagged with it.
    """
    enum_tags: List[Dict[str, Any]]
    """Unique String identifier"""
    identifier: str
    """Distance in pixels from image borders"""
    padding: int
    """Image height in pixels"""
    px_hei: int
    """Image width in pixels"""
    px_wid: int
    """Path to the source file, relative to the current project JSON file"""
    rel_path: str
    """Array of group of tiles selections, only meant to be used in the editor"""
    saved_selections: List[Dict[str, Any]]
    """Space in pixels between all tiles"""
    spacing: int
    """Optional Enum definition UID used for this tileset meta-data"""
    tags_source_enum_uid: Optional[int]
    tile_grid_size: int
    """Unique Intidentifier"""
    uid: int

    def __init__(self, c_hei: int, c_wid: int, cached_pixel_data: Optional[Dict[str, Any]], custom_data: List[Dict[str, Any]], enum_tags: List[Dict[str, Any]], identifier: str, padding: int, px_hei: int, px_wid: int, rel_path: str, saved_selections: List[Dict[str, Any]], spacing: int, tags_source_enum_uid: Optional[int], tile_grid_size: int, uid: int) -> None:
        self.c_hei = c_hei
        self.c_wid = c_wid
        self.cached_pixel_data = cached_pixel_data
        self.custom_data = custom_data
        self.enum_tags = enum_tags
        self.identifier = identifier
        self.padding = padding
        self.px_hei = px_hei
        self.px_wid = px_wid
        self.rel_path = rel_path
        self.saved_selections = saved_selections
        self.spacing = spacing
        self.tags_source_enum_uid = tags_source_enum_uid
        self.tile_grid_size = tile_grid_size
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'TilesetDefinition':
        assert isinstance(obj, dict)
        c_hei = from_int(obj.get("__cHei"))
        c_wid = from_int(obj.get("__cWid"))
        cached_pixel_data = from_union([from_none, lambda x: from_dict(lambda x: x, x)], obj.get("cachedPixelData"))
        custom_data = from_list(lambda x: from_dict(lambda x: x, x), obj.get("customData"))
        enum_tags = from_list(lambda x: from_dict(lambda x: x, x), obj.get("enumTags"))
        identifier = from_str(obj.get("identifier"))
        padding = from_int(obj.get("padding"))
        px_hei = from_int(obj.get("pxHei"))
        px_wid = from_int(obj.get("pxWid"))
        rel_path = from_str(obj.get("relPath"))
        saved_selections = from_list(lambda x: from_dict(lambda x: x, x), obj.get("savedSelections"))
        spacing = from_int(obj.get("spacing"))
        tags_source_enum_uid = from_union([from_none, from_int], obj.get("tagsSourceEnumUid"))
        tile_grid_size = from_int(obj.get("tileGridSize"))
        uid = from_int(obj.get("uid"))
        return TilesetDefinition(c_hei, c_wid, cached_pixel_data, custom_data, enum_tags, identifier, padding, px_hei, px_wid, rel_path, saved_selections, spacing, tags_source_enum_uid, tile_grid_size, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_int(self.c_hei)
        result["__cWid"] = from_int(self.c_wid)
        result["cachedPixelData"] = from_union([from_none, lambda x: from_dict(lambda x: x, x)], self.cached_pixel_data)
        result["customData"] = from_list(lambda x: from_dict(lambda x: x, x), self.custom_data)
        result["enumTags"] = from_list(lambda x: from_dict(lambda x: x, x), self.enum_tags)
        result["identifier"] = from_str(self.identifier)
        result["padding"] = from_int(self.padding)
        result["pxHei"] = from_int(self.px_hei)
        result["pxWid"] = from_int(self.px_wid)
        result["relPath"] = from_str(self.rel_path)
        result["savedSelections"] = from_list(lambda x: from_dict(lambda x: x, x), self.saved_selections)
        result["spacing"] = from_int(self.spacing)
        result["tagsSourceEnumUid"] = from_union([from_none, from_int], self.tags_source_enum_uid)
        result["tileGridSize"] = from_int(self.tile_grid_size)
        result["uid"] = from_int(self.uid)
        return result


class Definitions:
    """A structure containing all the definitions of this project
    
    If you're writing your own LDtk importer, you should probably just ignore *most* stuff in
    the `defs` section, as it contains data that are mostly important to the editor. To keep
    you away from the `defs` section and avoid some unnecessary JSON parsing, important data
    from definitions is often duplicated in fields prefixed with a double underscore (eg.
    `__identifier` or `__type`).  The 2 only definition types you might need here are
    **Tilesets** and **Enums**.
    """
    """All entities, including their custom fields"""
    entities: List[EntityDefinition]
    enums: List[EnumDefinition]
    """Note: external enums are exactly the same as `enums`, except they have a `relPath` to
    point to an external source file.
    """
    external_enums: List[EnumDefinition]
    layers: List[LayerDefinition]
    """An array containing all custom fields available to all levels."""
    level_fields: List[FieldDefinition]
    tilesets: List[TilesetDefinition]

    def __init__(self, entities: List[EntityDefinition], enums: List[EnumDefinition], external_enums: List[EnumDefinition], layers: List[LayerDefinition], level_fields: List[FieldDefinition], tilesets: List[TilesetDefinition]) -> None:
        self.entities = entities
        self.enums = enums
        self.external_enums = external_enums
        self.layers = layers
        self.level_fields = level_fields
        self.tilesets = tilesets

    @staticmethod
    def from_dict(obj: Any) -> 'Definitions':
        assert isinstance(obj, dict)
        entities = from_list(EntityDefinition.from_dict, obj.get("entities"))
        enums = from_list(EnumDefinition.from_dict, obj.get("enums"))
        external_enums = from_list(EnumDefinition.from_dict, obj.get("externalEnums"))
        layers = from_list(LayerDefinition.from_dict, obj.get("layers"))
        level_fields = from_list(FieldDefinition.from_dict, obj.get("levelFields"))
        tilesets = from_list(TilesetDefinition.from_dict, obj.get("tilesets"))
        return Definitions(entities, enums, external_enums, layers, level_fields, tilesets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_list(lambda x: to_class(EntityDefinition, x), self.entities)
        result["enums"] = from_list(lambda x: to_class(EnumDefinition, x), self.enums)
        result["externalEnums"] = from_list(lambda x: to_class(EnumDefinition, x), self.external_enums)
        result["layers"] = from_list(lambda x: to_class(LayerDefinition, x), self.layers)
        result["levelFields"] = from_list(lambda x: to_class(FieldDefinition, x), self.level_fields)
        result["tilesets"] = from_list(lambda x: to_class(TilesetDefinition, x), self.tilesets)
        return result


class Flag(Enum):
    DISCARD_PRE_CSV_INT_GRID = "DiscardPreCsvIntGrid"
    IGNORE_BACKUP_SUGGEST = "IgnoreBackupSuggest"


class LevelBackgroundPosition:
    """Level background image position info"""
    """An array of 4 float values describing the cropped sub-rectangle of the displayed
    background image. This cropping happens when original is larger than the level bounds.
    Array format: `[ cropX, cropY, cropWidth, cropHeight ]`
    """
    crop_rect: List[float]
    """An array containing the `[scaleX,scaleY]` values of the **cropped** background image,
    depending on `bgPos` option.
    """
    scale: List[float]
    """An array containing the `[x,y]` pixel coordinates of the top-left corner of the
    **cropped** background image, depending on `bgPos` option.
    """
    top_left_px: List[int]

    def __init__(self, crop_rect: List[float], scale: List[float], top_left_px: List[int]) -> None:
        self.crop_rect = crop_rect
        self.scale = scale
        self.top_left_px = top_left_px

    @staticmethod
    def from_dict(obj: Any) -> 'LevelBackgroundPosition':
        assert isinstance(obj, dict)
        crop_rect = from_list(from_float, obj.get("cropRect"))
        scale = from_list(from_float, obj.get("scale"))
        top_left_px = from_list(from_int, obj.get("topLeftPx"))
        return LevelBackgroundPosition(crop_rect, scale, top_left_px)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cropRect"] = from_list(to_float, self.crop_rect)
        result["scale"] = from_list(to_float, self.scale)
        result["topLeftPx"] = from_list(from_int, self.top_left_px)
        return result


class FieldInstance:
    """Field definition identifier"""
    identifier: str
    """Type of the field, such as `Int`, `Float`, `Enum(my_enum_name)`, `Bool`, etc."""
    type: str
    """Actual value of the field instance. The value type may vary, depending on `__type`
    (Integer, Boolean, String etc.)<br/>  It can also be an `Array` of those same types.
    """
    value: Any
    """Reference of the **Field definition** UID"""
    def_uid: int
    """Editor internal raw values"""
    real_editor_values: List[Any]

    def __init__(self, identifier: str, type: str, value: Any, def_uid: int, real_editor_values: List[Any]) -> None:
        self.identifier = identifier
        self.type = type
        self.value = value
        self.def_uid = def_uid
        self.real_editor_values = real_editor_values

    @staticmethod
    def from_dict(obj: Any) -> 'FieldInstance':
        assert isinstance(obj, dict)
        identifier = from_str(obj.get("__identifier"))
        type = from_str(obj.get("__type"))
        value = obj.get("__value")
        def_uid = from_int(obj.get("defUid"))
        real_editor_values = from_list(lambda x: x, obj.get("realEditorValues"))
        return FieldInstance(identifier, type, value, def_uid, real_editor_values)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__identifier"] = from_str(self.identifier)
        result["__type"] = from_str(self.type)
        result["__value"] = self.value
        result["defUid"] = from_int(self.def_uid)
        result["realEditorValues"] = from_list(lambda x: x, self.real_editor_values)
        return result


class TileInstance:
    """This structure represents a single tile from a given Tileset."""
    """Internal data used by the editor.<br/>  For auto-layer tiles: `[ruleId, coordId]`.<br/>
    For tile-layer tiles: `[coordId]`.
    """
    d: List[int]
    """"Flip bits", a 2-bits integer to represent the mirror transformations of the tile.<br/>
    - Bit 0 = X flip<br/>   - Bit 1 = Y flip<br/>   Examples: f=0 (no flip), f=1 (X flip
    only), f=2 (Y flip only), f=3 (both flips)
    """
    f: int
    """Pixel coordinates of the tile in the **layer** (`[x,y]` format). Don't forget optional
    layer offsets, if they exist!
    """
    px: List[int]
    """Pixel coordinates of the tile in the **tileset** (`[x,y]` format)"""
    src: List[int]
    """The *Tile ID* in the corresponding tileset."""
    t: int

    def __init__(self, d: List[int], f: int, px: List[int], src: List[int], t: int) -> None:
        self.d = d
        self.f = f
        self.px = px
        self.src = src
        self.t = t

    @staticmethod
    def from_dict(obj: Any) -> 'TileInstance':
        assert isinstance(obj, dict)
        d = from_list(from_int, obj.get("d"))
        f = from_int(obj.get("f"))
        px = from_list(from_int, obj.get("px"))
        src = from_list(from_int, obj.get("src"))
        t = from_int(obj.get("t"))
        return TileInstance(d, f, px, src, t)

    def to_dict(self) -> dict:
        result: dict = {}
        result["d"] = from_list(from_int, self.d)
        result["f"] = from_int(self.f)
        result["px"] = from_list(from_int, self.px)
        result["src"] = from_list(from_int, self.src)
        result["t"] = from_int(self.t)
        return result


class EntityInstanceTile:
    """Tile data in an Entity instance"""
    """An array of 4 Int values that refers to the tile in the tileset image: `[ x, y, width,
    height ]`
    """
    src_rect: List[int]
    """Tileset ID"""
    tileset_uid: int

    def __init__(self, src_rect: List[int], tileset_uid: int) -> None:
        self.src_rect = src_rect
        self.tileset_uid = tileset_uid

    @staticmethod
    def from_dict(obj: Any) -> 'EntityInstanceTile':
        assert isinstance(obj, dict)
        src_rect = from_list(from_int, obj.get("srcRect"))
        tileset_uid = from_int(obj.get("tilesetUid"))
        return EntityInstanceTile(src_rect, tileset_uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["srcRect"] = from_list(from_int, self.src_rect)
        result["tilesetUid"] = from_int(self.tileset_uid)
        return result


class EntityInstance:
    """Grid-based coordinates (`[x,y]` format)"""
    grid: List[int]
    """Entity definition identifier"""
    identifier: str
    """Pivot coordinates  (`[x,y]` format, values are from 0 to 1) of the Entity"""
    pivot: List[float]
    """Optional Tile used to display this entity (it could either be the default Entity tile, or
    some tile provided by a field value, like an Enum).
    """
    tile: Optional[EntityInstanceTile]
    """Reference of the **Entity definition** UID"""
    def_uid: int
    """An array of all custom fields and their values."""
    field_instances: List[FieldInstance]
    """Entity height in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    height: int
    """Pixel coordinates (`[x,y]` format) in current level coordinate space. Don't forget
    optional layer offsets, if they exist!
    """
    px: List[int]
    """Entity width in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    width: int

    def __init__(self, grid: List[int], identifier: str, pivot: List[float], tile: Optional[EntityInstanceTile], def_uid: int, field_instances: List[FieldInstance], height: int, px: List[int], width: int) -> None:
        self.grid = grid
        self.identifier = identifier
        self.pivot = pivot
        self.tile = tile
        self.def_uid = def_uid
        self.field_instances = field_instances
        self.height = height
        self.px = px
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'EntityInstance':
        assert isinstance(obj, dict)
        grid = from_list(from_int, obj.get("__grid"))
        identifier = from_str(obj.get("__identifier"))
        pivot = from_list(from_float, obj.get("__pivot"))
        tile = from_union([from_none, EntityInstanceTile.from_dict], obj.get("__tile"))
        def_uid = from_int(obj.get("defUid"))
        field_instances = from_list(FieldInstance.from_dict, obj.get("fieldInstances"))
        height = from_int(obj.get("height"))
        px = from_list(from_int, obj.get("px"))
        width = from_int(obj.get("width"))
        return EntityInstance(grid, identifier, pivot, tile, def_uid, field_instances, height, px, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__grid"] = from_list(from_int, self.grid)
        result["__identifier"] = from_str(self.identifier)
        result["__pivot"] = from_list(to_float, self.pivot)
        result["__tile"] = from_union([from_none, lambda x: to_class(EntityInstanceTile, x)], self.tile)
        result["defUid"] = from_int(self.def_uid)
        result["fieldInstances"] = from_list(lambda x: to_class(FieldInstance, x), self.field_instances)
        result["height"] = from_int(self.height)
        result["px"] = from_list(from_int, self.px)
        result["width"] = from_int(self.width)
        return result


class IntGridValueInstance:
    """IntGrid value instance"""
    """Coordinate ID in the layer grid"""
    coord_id: int
    """IntGrid value"""
    v: int

    def __init__(self, coord_id: int, v: int) -> None:
        self.coord_id = coord_id
        self.v = v

    @staticmethod
    def from_dict(obj: Any) -> 'IntGridValueInstance':
        assert isinstance(obj, dict)
        coord_id = from_int(obj.get("coordId"))
        v = from_int(obj.get("v"))
        return IntGridValueInstance(coord_id, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordId"] = from_int(self.coord_id)
        result["v"] = from_int(self.v)
        return result


class LayerInstance:
    """Grid-based height"""
    c_hei: int
    """Grid-based width"""
    c_wid: int
    """Grid size"""
    grid_size: int
    """Layer definition identifier"""
    identifier: str
    """Layer opacity as Float [0-1]"""
    opacity: float
    """Total layer X pixel offset, including both instance and definition offsets."""
    px_total_offset_x: int
    """Total layer Y pixel offset, including both instance and definition offsets."""
    px_total_offset_y: int
    """The definition UID of corresponding Tileset, if any."""
    tileset_def_uid: Optional[int]
    """The relative path to corresponding Tileset, if any."""
    tileset_rel_path: Optional[str]
    """Layer type (possible values: IntGrid, Entities, Tiles or AutoLayer)"""
    type: str
    """An array containing all tiles generated by Auto-layer rules. The array is already sorted
    in display order (ie. 1st tile is beneath 2nd, which is beneath 3rd etc.).<br/><br/>
    Note: if multiple tiles are stacked in the same cell as the result of different rules,
    all tiles behind opaque ones will be discarded.
    """
    auto_layer_tiles: List[TileInstance]
    entity_instances: List[EntityInstance]
    grid_tiles: List[TileInstance]
    """**WARNING**: this deprecated value will be *removed* completely on version 0.10.0+
    Replaced by: `intGridCsv`
    """
    int_grid: Optional[List[IntGridValueInstance]]
    """A list of all values in the IntGrid layer, stored from left to right, and top to bottom
    (ie. first row from left to right, followed by second row, etc). `0` means "empty cell"
    and IntGrid values start at 1. This array size is `__cWid` x `__cHei` cells.
    """
    int_grid_csv: List[int]
    """Reference the Layer definition UID"""
    layer_def_uid: int
    """Reference to the UID of the level containing this layer instance"""
    level_id: int
    """An Array containing the UIDs of optional rules that were enabled in this specific layer
    instance.
    """
    optional_rules: List[int]
    """This layer can use another tileset by overriding the tileset UID here."""
    override_tileset_uid: Optional[int]
    """X offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetX`)
    """
    px_offset_x: int
    """Y offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetY`)
    """
    px_offset_y: int
    """Random seed used for Auto-Layers rendering"""
    seed: int
    """Layer instance visibility"""
    visible: bool

    def __init__(self, c_hei: int, c_wid: int, grid_size: int, identifier: str, opacity: float, px_total_offset_x: int, px_total_offset_y: int, tileset_def_uid: Optional[int], tileset_rel_path: Optional[str], type: str, auto_layer_tiles: List[TileInstance], entity_instances: List[EntityInstance], grid_tiles: List[TileInstance], int_grid: Optional[List[IntGridValueInstance]], int_grid_csv: List[int], layer_def_uid: int, level_id: int, optional_rules: List[int], override_tileset_uid: Optional[int], px_offset_x: int, px_offset_y: int, seed: int, visible: bool) -> None:
        self.c_hei = c_hei
        self.c_wid = c_wid
        self.grid_size = grid_size
        self.identifier = identifier
        self.opacity = opacity
        self.px_total_offset_x = px_total_offset_x
        self.px_total_offset_y = px_total_offset_y
        self.tileset_def_uid = tileset_def_uid
        self.tileset_rel_path = tileset_rel_path
        self.type = type
        self.auto_layer_tiles = auto_layer_tiles
        self.entity_instances = entity_instances
        self.grid_tiles = grid_tiles
        self.int_grid = int_grid
        self.int_grid_csv = int_grid_csv
        self.layer_def_uid = layer_def_uid
        self.level_id = level_id
        self.optional_rules = optional_rules
        self.override_tileset_uid = override_tileset_uid
        self.px_offset_x = px_offset_x
        self.px_offset_y = px_offset_y
        self.seed = seed
        self.visible = visible

    @staticmethod
    def from_dict(obj: Any) -> 'LayerInstance':
        assert isinstance(obj, dict)
        c_hei = from_int(obj.get("__cHei"))
        c_wid = from_int(obj.get("__cWid"))
        grid_size = from_int(obj.get("__gridSize"))
        identifier = from_str(obj.get("__identifier"))
        opacity = from_float(obj.get("__opacity"))
        px_total_offset_x = from_int(obj.get("__pxTotalOffsetX"))
        px_total_offset_y = from_int(obj.get("__pxTotalOffsetY"))
        tileset_def_uid = from_union([from_none, from_int], obj.get("__tilesetDefUid"))
        tileset_rel_path = from_union([from_none, from_str], obj.get("__tilesetRelPath"))
        type = from_str(obj.get("__type"))
        auto_layer_tiles = from_list(TileInstance.from_dict, obj.get("autoLayerTiles"))
        entity_instances = from_list(EntityInstance.from_dict, obj.get("entityInstances"))
        grid_tiles = from_list(TileInstance.from_dict, obj.get("gridTiles"))
        int_grid = from_union([lambda x: from_list(IntGridValueInstance.from_dict, x), from_none], obj.get("intGrid"))
        int_grid_csv = from_list(from_int, obj.get("intGridCsv"))
        layer_def_uid = from_int(obj.get("layerDefUid"))
        level_id = from_int(obj.get("levelId"))
        optional_rules = from_list(from_int, obj.get("optionalRules"))
        override_tileset_uid = from_union([from_none, from_int], obj.get("overrideTilesetUid"))
        px_offset_x = from_int(obj.get("pxOffsetX"))
        px_offset_y = from_int(obj.get("pxOffsetY"))
        seed = from_int(obj.get("seed"))
        visible = from_bool(obj.get("visible"))
        return LayerInstance(c_hei, c_wid, grid_size, identifier, opacity, px_total_offset_x, px_total_offset_y, tileset_def_uid, tileset_rel_path, type, auto_layer_tiles, entity_instances, grid_tiles, int_grid, int_grid_csv, layer_def_uid, level_id, optional_rules, override_tileset_uid, px_offset_x, px_offset_y, seed, visible)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_int(self.c_hei)
        result["__cWid"] = from_int(self.c_wid)
        result["__gridSize"] = from_int(self.grid_size)
        result["__identifier"] = from_str(self.identifier)
        result["__opacity"] = to_float(self.opacity)
        result["__pxTotalOffsetX"] = from_int(self.px_total_offset_x)
        result["__pxTotalOffsetY"] = from_int(self.px_total_offset_y)
        result["__tilesetDefUid"] = from_union([from_none, from_int], self.tileset_def_uid)
        result["__tilesetRelPath"] = from_union([from_none, from_str], self.tileset_rel_path)
        result["__type"] = from_str(self.type)
        result["autoLayerTiles"] = from_list(lambda x: to_class(TileInstance, x), self.auto_layer_tiles)
        result["entityInstances"] = from_list(lambda x: to_class(EntityInstance, x), self.entity_instances)
        result["gridTiles"] = from_list(lambda x: to_class(TileInstance, x), self.grid_tiles)
        result["intGrid"] = from_union([lambda x: from_list(lambda x: to_class(IntGridValueInstance, x), x), from_none], self.int_grid)
        result["intGridCsv"] = from_list(from_int, self.int_grid_csv)
        result["layerDefUid"] = from_int(self.layer_def_uid)
        result["levelId"] = from_int(self.level_id)
        result["optionalRules"] = from_list(from_int, self.optional_rules)
        result["overrideTilesetUid"] = from_union([from_none, from_int], self.override_tileset_uid)
        result["pxOffsetX"] = from_int(self.px_offset_x)
        result["pxOffsetY"] = from_int(self.px_offset_y)
        result["seed"] = from_int(self.seed)
        result["visible"] = from_bool(self.visible)
        return result


class BgPos(Enum):
    CONTAIN = "Contain"
    COVER = "Cover"
    COVER_DIRTY = "CoverDirty"
    UNSCALED = "Unscaled"


class NeighbourLevel:
    """Nearby level info"""
    """A single lowercase character tipping on the level location (`n`orth, `s`outh, `w`est,
    `e`ast).
    """
    dir: str
    level_uid: int

    def __init__(self, dir: str, level_uid: int) -> None:
        self.dir = dir
        self.level_uid = level_uid

    @staticmethod
    def from_dict(obj: Any) -> 'NeighbourLevel':
        assert isinstance(obj, dict)
        dir = from_str(obj.get("dir"))
        level_uid = from_int(obj.get("levelUid"))
        return NeighbourLevel(dir, level_uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dir"] = from_str(self.dir)
        result["levelUid"] = from_int(self.level_uid)
        return result


class Level:
    """This section contains all the level data. It can be found in 2 distinct forms, depending
    on Project current settings:  - If "*Separate level files*" is **disabled** (default):
    full level data is *embedded* inside the main Project JSON file, - If "*Separate level
    files*" is **enabled**: level data is stored in *separate* standalone `.ldtkl` files (one
    per level). In this case, the main Project JSON file will still contain most level data,
    except heavy sections, like the `layerInstances` array (which will be null). The
    `externalRelPath` string points to the `ldtkl` file.  A `ldtkl` file is just a JSON file
    containing exactly what is described below.
    """
    """Background color of the level (same as `bgColor`, except the default value is
    automatically used here if its value is `null`)
    """
    bg_color: str
    """Position informations of the background image, if there is one."""
    bg_pos: Optional[LevelBackgroundPosition]
    """An array listing all other levels touching this one on the world map. In "linear" world
    layouts, this array is populated with previous/next levels in array, and `dir` depends on
    the linear horizontal/vertical layout.
    """
    neighbours: List[NeighbourLevel]
    """Background color of the level. If `null`, the project `defaultLevelBgColor` should be
    used.
    """
    level_bg_color: Optional[str]
    """Background image X pivot (0-1)"""
    bg_pivot_x: float
    """Background image Y pivot (0-1)"""
    bg_pivot_y: float
    """An enum defining the way the background image (if any) is positioned on the level. See
    `__bgPos` for resulting position info. Possible values: &lt;`null`&gt;, `Unscaled`,
    `Contain`, `Cover`, `CoverDirty`
    """
    level_bg_pos: Optional[BgPos]
    """The *optional* relative path to the level background image."""
    bg_rel_path: Optional[str]
    """This value is not null if the project option "*Save levels separately*" is enabled. In
    this case, this **relative** path points to the level Json file.
    """
    external_rel_path: Optional[str]
    """An array containing this level custom field values."""
    field_instances: List[FieldInstance]
    """Unique String identifier"""
    identifier: str
    """An array containing all Layer instances. **IMPORTANT**: if the project option "*Save
    levels separately*" is enabled, this field will be `null`.<br/>  This array is **sorted
    in display order**: the 1st layer is the top-most and the last is behind.
    """
    layer_instances: Optional[List[LayerInstance]]
    """Height of the level in pixels"""
    px_hei: int
    """Width of the level in pixels"""
    px_wid: int
    """Unique Int identifier"""
    uid: int
    """If TRUE, the level identifier will always automatically use the naming pattern as defined
    in `Project.levelNamePattern`. Becomes FALSE if the identifier is manually modified by
    user.
    """
    use_auto_identifier: bool
    """World X coordinate in pixels"""
    world_x: int
    """World Y coordinate in pixels"""
    world_y: int

    def __init__(self, bg_color: str, bg_pos: Optional[LevelBackgroundPosition], neighbours: List[NeighbourLevel], level_bg_color: Optional[str], bg_pivot_x: float, bg_pivot_y: float, level_bg_pos: Optional[BgPos], bg_rel_path: Optional[str], external_rel_path: Optional[str], field_instances: List[FieldInstance], identifier: str, layer_instances: Optional[List[LayerInstance]], px_hei: int, px_wid: int, uid: int, use_auto_identifier: bool, world_x: int, world_y: int) -> None:
        self.bg_color = bg_color
        self.bg_pos = bg_pos
        self.neighbours = neighbours
        self.level_bg_color = level_bg_color
        self.bg_pivot_x = bg_pivot_x
        self.bg_pivot_y = bg_pivot_y
        self.level_bg_pos = level_bg_pos
        self.bg_rel_path = bg_rel_path
        self.external_rel_path = external_rel_path
        self.field_instances = field_instances
        self.identifier = identifier
        self.layer_instances = layer_instances
        self.px_hei = px_hei
        self.px_wid = px_wid
        self.uid = uid
        self.use_auto_identifier = use_auto_identifier
        self.world_x = world_x
        self.world_y = world_y

    @staticmethod
    def from_dict(obj: Any) -> 'Level':
        assert isinstance(obj, dict)
        bg_color = from_str(obj.get("__bgColor"))
        bg_pos = from_union([from_none, LevelBackgroundPosition.from_dict], obj.get("__bgPos"))
        neighbours = from_list(NeighbourLevel.from_dict, obj.get("__neighbours"))
        level_bg_color = from_union([from_none, from_str], obj.get("bgColor"))
        bg_pivot_x = from_float(obj.get("bgPivotX"))
        bg_pivot_y = from_float(obj.get("bgPivotY"))
        level_bg_pos = from_union([from_none, BgPos], obj.get("bgPos"))
        bg_rel_path = from_union([from_none, from_str], obj.get("bgRelPath"))
        external_rel_path = from_union([from_none, from_str], obj.get("externalRelPath"))
        field_instances = from_list(FieldInstance.from_dict, obj.get("fieldInstances"))
        identifier = from_str(obj.get("identifier"))
        layer_instances = from_union([from_none, lambda x: from_list(LayerInstance.from_dict, x)], obj.get("layerInstances"))
        px_hei = from_int(obj.get("pxHei"))
        px_wid = from_int(obj.get("pxWid"))
        uid = from_int(obj.get("uid"))
        use_auto_identifier = from_bool(obj.get("useAutoIdentifier"))
        world_x = from_int(obj.get("worldX"))
        world_y = from_int(obj.get("worldY"))
        return Level(bg_color, bg_pos, neighbours, level_bg_color, bg_pivot_x, bg_pivot_y, level_bg_pos, bg_rel_path, external_rel_path, field_instances, identifier, layer_instances, px_hei, px_wid, uid, use_auto_identifier, world_x, world_y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__bgColor"] = from_str(self.bg_color)
        result["__bgPos"] = from_union([from_none, lambda x: to_class(LevelBackgroundPosition, x)], self.bg_pos)
        result["__neighbours"] = from_list(lambda x: to_class(NeighbourLevel, x), self.neighbours)
        result["bgColor"] = from_union([from_none, from_str], self.level_bg_color)
        result["bgPivotX"] = to_float(self.bg_pivot_x)
        result["bgPivotY"] = to_float(self.bg_pivot_y)
        result["bgPos"] = from_union([from_none, lambda x: to_enum(BgPos, x)], self.level_bg_pos)
        result["bgRelPath"] = from_union([from_none, from_str], self.bg_rel_path)
        result["externalRelPath"] = from_union([from_none, from_str], self.external_rel_path)
        result["fieldInstances"] = from_list(lambda x: to_class(FieldInstance, x), self.field_instances)
        result["identifier"] = from_str(self.identifier)
        result["layerInstances"] = from_union([from_none, lambda x: from_list(lambda x: to_class(LayerInstance, x), x)], self.layer_instances)
        result["pxHei"] = from_int(self.px_hei)
        result["pxWid"] = from_int(self.px_wid)
        result["uid"] = from_int(self.uid)
        result["useAutoIdentifier"] = from_bool(self.use_auto_identifier)
        result["worldX"] = from_int(self.world_x)
        result["worldY"] = from_int(self.world_y)
        return result


class WorldLayout(Enum):
    """An enum that describes how levels are organized in this project (ie. linearly or in a 2D
    space). Possible values: `Free`, `GridVania`, `LinearHorizontal`, `LinearVertical`
    """
    FREE = "Free"
    GRID_VANIA = "GridVania"
    LINEAR_HORIZONTAL = "LinearHorizontal"
    LINEAR_VERTICAL = "LinearVertical"


class LdtkJSON:
    """This file is a JSON schema of files created by LDtk level editor (https://ldtk.io).
    
    This is the root of any Project JSON file. It contains:  - the project settings, - an
    array of levels, - and a definition object (that can probably be safely ignored for most
    users).
    """
    """Number of backup files to keep, if the `backupOnSave` is TRUE"""
    backup_limit: int
    """If TRUE, an extra copy of the project will be created in a sub folder, when saving."""
    backup_on_save: bool
    """Project background color"""
    bg_color: str
    """Default grid size for new layers"""
    default_grid_size: int
    """Default background color of levels"""
    default_level_bg_color: str
    """Default new level height"""
    default_level_height: int
    """Default new level width"""
    default_level_width: int
    """Default X pivot (0 to 1) for new entities"""
    default_pivot_x: float
    """Default Y pivot (0 to 1) for new entities"""
    default_pivot_y: float
    """A structure containing all the definitions of this project"""
    defs: Definitions
    """If TRUE, all layers in all levels will also be exported as PNG along with the project
    file (default is FALSE)
    """
    export_png: bool
    """If TRUE, a Tiled compatible file will also be generated along with the LDtk JSON file
    (default is FALSE)
    """
    export_tiled: bool
    """If TRUE, one file will be saved for the project (incl. all its definitions) and one file
    in a sub-folder for each level.
    """
    external_levels: bool
    """An array containing various advanced flags (ie. options or other states). Possible
    values: `DiscardPreCsvIntGrid`, `IgnoreBackupSuggest`
    """
    flags: List[Flag]
    """File format version"""
    json_version: str
    """The default naming convention for level identifiers."""
    level_name_pattern: str
    """All levels. The order of this array is only relevant in `LinearHorizontal` and
    `linearVertical` world layouts (see `worldLayout` value). Otherwise, you should refer to
    the `worldX`,`worldY` coordinates of each Level.
    """
    levels: List[Level]
    """If TRUE, the Json is partially minified (no indentation, nor line breaks, default is
    FALSE)
    """
    minify_json: bool
    """Next Unique integer ID available"""
    next_uid: int
    """File naming pattern for exported PNGs"""
    png_file_pattern: Optional[str]
    """Height of the world grid in pixels."""
    world_grid_height: int
    """Width of the world grid in pixels."""
    world_grid_width: int
    """An enum that describes how levels are organized in this project (ie. linearly or in a 2D
    space). Possible values: `Free`, `GridVania`, `LinearHorizontal`, `LinearVertical`
    """
    world_layout: WorldLayout

    def __init__(self, backup_limit: int, backup_on_save: bool, bg_color: str, default_grid_size: int, default_level_bg_color: str, default_level_height: int, default_level_width: int, default_pivot_x: float, default_pivot_y: float, defs: Definitions, export_png: bool, export_tiled: bool, external_levels: bool, flags: List[Flag], json_version: str, level_name_pattern: str, levels: List[Level], minify_json: bool, next_uid: int, png_file_pattern: Optional[str], world_grid_height: int, world_grid_width: int, world_layout: WorldLayout) -> None:
        self.backup_limit = backup_limit
        self.backup_on_save = backup_on_save
        self.bg_color = bg_color
        self.default_grid_size = default_grid_size
        self.default_level_bg_color = default_level_bg_color
        self.default_level_height = default_level_height
        self.default_level_width = default_level_width
        self.default_pivot_x = default_pivot_x
        self.default_pivot_y = default_pivot_y
        self.defs = defs
        self.export_png = export_png
        self.export_tiled = export_tiled
        self.external_levels = external_levels
        self.flags = flags
        self.json_version = json_version
        self.level_name_pattern = level_name_pattern
        self.levels = levels
        self.minify_json = minify_json
        self.next_uid = next_uid
        self.png_file_pattern = png_file_pattern
        self.world_grid_height = world_grid_height
        self.world_grid_width = world_grid_width
        self.world_layout = world_layout

    @staticmethod
    def from_dict(obj: Any) -> 'LdtkJSON':
        assert isinstance(obj, dict)
        backup_limit = from_int(obj.get("backupLimit"))
        backup_on_save = from_bool(obj.get("backupOnSave"))
        bg_color = from_str(obj.get("bgColor"))
        default_grid_size = from_int(obj.get("defaultGridSize"))
        default_level_bg_color = from_str(obj.get("defaultLevelBgColor"))
        default_level_height = from_int(obj.get("defaultLevelHeight"))
        default_level_width = from_int(obj.get("defaultLevelWidth"))
        default_pivot_x = from_float(obj.get("defaultPivotX"))
        default_pivot_y = from_float(obj.get("defaultPivotY"))
        defs = Definitions.from_dict(obj.get("defs"))
        export_png = from_bool(obj.get("exportPng"))
        export_tiled = from_bool(obj.get("exportTiled"))
        external_levels = from_bool(obj.get("externalLevels"))
        flags = from_list(Flag, obj.get("flags"))
        json_version = from_str(obj.get("jsonVersion"))
        level_name_pattern = from_str(obj.get("levelNamePattern"))
        levels = from_list(Level.from_dict, obj.get("levels"))
        minify_json = from_bool(obj.get("minifyJson"))
        next_uid = from_int(obj.get("nextUid"))
        png_file_pattern = from_union([from_none, from_str], obj.get("pngFilePattern"))
        world_grid_height = from_int(obj.get("worldGridHeight"))
        world_grid_width = from_int(obj.get("worldGridWidth"))
        world_layout = WorldLayout(obj.get("worldLayout"))
        return LdtkJSON(backup_limit, backup_on_save, bg_color, default_grid_size, default_level_bg_color, default_level_height, default_level_width, default_pivot_x, default_pivot_y, defs, export_png, export_tiled, external_levels, flags, json_version, level_name_pattern, levels, minify_json, next_uid, png_file_pattern, world_grid_height, world_grid_width, world_layout)

    def to_dict(self) -> dict:
        result: dict = {}
        result["backupLimit"] = from_int(self.backup_limit)
        result["backupOnSave"] = from_bool(self.backup_on_save)
        result["bgColor"] = from_str(self.bg_color)
        result["defaultGridSize"] = from_int(self.default_grid_size)
        result["defaultLevelBgColor"] = from_str(self.default_level_bg_color)
        result["defaultLevelHeight"] = from_int(self.default_level_height)
        result["defaultLevelWidth"] = from_int(self.default_level_width)
        result["defaultPivotX"] = to_float(self.default_pivot_x)
        result["defaultPivotY"] = to_float(self.default_pivot_y)
        result["defs"] = to_class(Definitions, self.defs)
        result["exportPng"] = from_bool(self.export_png)
        result["exportTiled"] = from_bool(self.export_tiled)
        result["externalLevels"] = from_bool(self.external_levels)
        result["flags"] = from_list(lambda x: to_enum(Flag, x), self.flags)
        result["jsonVersion"] = from_str(self.json_version)
        result["levelNamePattern"] = from_str(self.level_name_pattern)
        result["levels"] = from_list(lambda x: to_class(Level, x), self.levels)
        result["minifyJson"] = from_bool(self.minify_json)
        result["nextUid"] = from_int(self.next_uid)
        result["pngFilePattern"] = from_union([from_none, from_str], self.png_file_pattern)
        result["worldGridHeight"] = from_int(self.world_grid_height)
        result["worldGridWidth"] = from_int(self.world_grid_width)
        result["worldLayout"] = to_enum(WorldLayout, self.world_layout)
        return result


def ldtk_json_from_dict(s: Any) -> LdtkJSON:
    return LdtkJSON.from_dict(s)


def ldtk_json_to_dict(x: LdtkJSON) -> Any:
    return to_class(LdtkJSON, x)
