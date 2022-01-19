import collections
import os

from binaryninja import (
    Architecture,
    BinaryView,
    SectionSemantics,
    SegmentFlag,
    Symbol,
    SymbolType,
    Platform,
)


class GBAPlatform(Platform):
    name = "gba-thumb2"


gba = GBAPlatform(Architecture["thumb2"])
gba.register("gba")
gba.default_calling_convention = Architecture[
    "thumb2"
].standalone_platform.default_calling_convention
gba.system_call_convention = Architecture[
    "thumb2"
].standalone_platform.calling_conventions[1]


Segment = collections.namedtuple("Segment", ["name", "start", "length", "flags"])
IOReg = collections.namedtuple("IOReg", ["name", "start", "length", "flags"])


R = SegmentFlag.SegmentReadable
W = SegmentFlag.SegmentWritable
X = SegmentFlag.SegmentExecutable

_SEGMENTS = [
    Segment("EWRAM", start=0x02000000, length=0x00040000, flags=R | W | X),
    Segment("IWRAM", start=0x03000000, length=0x00008000, flags=R | W | X),
    Segment("IO", start=0x03000000, length=0x000003FF, flags=R | W),
    Segment("PAL", start=0x05000000, length=0x00000400, flags=R | W),
    Segment("VRAM", start=0x06000000, length=0x00018000, flags=R | W),
    Segment("OAM", start=0x07000000, length=0x00000400, flags=R | W),
    Segment("SRAM", start=0x0E000000, length=0x00010000, flags=R | W),
]

_IOREGS = [
    IOReg("DISPCNT", start=0x04000000, length=2, flags=R | W),
    IOReg("DISPSTAT", start=0x04000004, length=2, flags=R | W),
    IOReg("VCOUNT", start=0x04000006, length=2, flags=R),
    IOReg("BG0CNT", start=0x04000008, length=2, flags=R | W),
    IOReg("BG1CNT", start=0x0400000A, length=2, flags=R | W),
    IOReg("BG2CNT", start=0x0400000C, length=2, flags=R | W),
    IOReg("BG3CNT", start=0x0400000E, length=2, flags=R | W),
    IOReg("BG0HOFS", start=0x04000010, length=2, flags=W),
    IOReg("BG0VOFS", start=0x04000012, length=2, flags=W),
    IOReg("BG1HOFS", start=0x04000014, length=2, flags=W),
    IOReg("BG1VOFS", start=0x04000016, length=2, flags=W),
    IOReg("BG2HOFS", start=0x04000018, length=2, flags=W),
    IOReg("BG2VOFS", start=0x0400001A, length=2, flags=W),
    IOReg("BG3HOFS", start=0x0400001C, length=2, flags=W),
    IOReg("BG3VOFS", start=0x0400001E, length=2, flags=W),
    IOReg("BG2PA", start=0x04000020, length=2, flags=W),
    IOReg("BG2PB", start=0x04000022, length=2, flags=W),
    IOReg("BG2PC", start=0x04000024, length=2, flags=W),
    IOReg("BG2PD", start=0x04000026, length=2, flags=W),
    IOReg("BG2X", start=0x04000028, length=4, flags=W),
    IOReg("BG2Y", start=0x0400002C, length=4, flags=W),
    IOReg("BG3PA", start=0x04000030, length=2, flags=W),
    IOReg("BG3PB", start=0x04000032, length=2, flags=W),
    IOReg("BG3PC", start=0x04000034, length=2, flags=W),
    IOReg("BG3PD", start=0x04000036, length=2, flags=W),
    IOReg("BG3X", start=0x04000038, length=4, flags=W),
    IOReg("BG3Y", start=0x0400003C, length=4, flags=W),
    IOReg("WIN0H", start=0x04000040, length=2, flags=W),
    IOReg("WIN1H", start=0x04000042, length=2, flags=W),
    IOReg("WIN0V", start=0x04000044, length=2, flags=W),
    IOReg("WIN1V", start=0x04000046, length=2, flags=W),
    IOReg("WININ", start=0x04000048, length=2, flags=R | W),
    IOReg("WINOUT", start=0x0400004A, length=2, flags=R | W),
    IOReg("MOSAIC", start=0x0400004C, length=2, flags=W),
    IOReg("BLDCNT", start=0x04000050, length=2, flags=R | W),
    IOReg("BLDALPHA", start=0x04000052, length=2, flags=R | W),
    IOReg("BLDY", start=0x04000054, length=2, flags=W),
    IOReg("SOUND1CNT_L", start=0x04000060, length=2, flags=R | W),
    IOReg("SOUND1CNT_H", start=0x04000062, length=2, flags=R | W),
    IOReg("SOUND1CNT_X", start=0x04000064, length=2, flags=R | W),
    IOReg("SOUND2CNT_L", start=0x04000068, length=2, flags=R | W),
    IOReg("SOUND2CNT_H", start=0x0400006C, length=2, flags=R | W),
    IOReg("SOUND3CNT_L", start=0x04000070, length=2, flags=R | W),
    IOReg("SOUND3CNT_H", start=0x04000072, length=2, flags=R | W),
    IOReg("SOUND3CNT_X", start=0x04000074, length=2, flags=R | W),
    IOReg("SOUND4CNT_L", start=0x04000078, length=2, flags=R | W),
    IOReg("SOUND4CNT_H", start=0x0400007C, length=2, flags=R | W),
    IOReg("SOUNDCNT_L", start=0x04000080, length=2, flags=R | W),
    IOReg("SOUNDCNT_H", start=0x04000082, length=2, flags=R | W),
    IOReg("SOUNDCNT_X", start=0x04000084, length=2, flags=R | W),
    IOReg("FIFO_A", start=0x040000A0, length=4, flags=W),
    IOReg("FIFO_B", start=0x040000A4, length=4, flags=W),
    IOReg("DMA0SAD", start=0x040000B0, length=4, flags=W),
    IOReg("DMA0DAD", start=0x040000B4, length=4, flags=W),
    IOReg("DMA0CNT_L", start=0x040000B8, length=2, flags=W),
    IOReg("DMA0CNT_H", start=0x040000BA, length=2, flags=R | W),
    IOReg("DMA1SAD", start=0x040000BC, length=4, flags=W),
    IOReg("DMA1DAD", start=0x040000C0, length=4, flags=W),
    IOReg("DMA1CNT_L", start=0x040000C4, length=2, flags=W),
    IOReg("DMA1CNT_H", start=0x040000C6, length=2, flags=R | W),
    IOReg("DMA2SAD", start=0x040000C8, length=4, flags=W),
    IOReg("DMA2DAD", start=0x040000CC, length=4, flags=W),
    IOReg("DMA2CNT_L", start=0x040000D0, length=2, flags=W),
    IOReg("DMA2CNT_H", start=0x040000D2, length=2, flags=R | W),
    IOReg("DMA3SAD", start=0x040000D4, length=4, flags=W),
    IOReg("DMA3DAD", start=0x040000D8, length=4, flags=W),
    IOReg("DMA3CNT_L", start=0x040000DC, length=2, flags=W),
    IOReg("DMA3CNT_H", start=0x040000DE, length=2, flags=R | W),
    IOReg("TM0CNT_L", start=0x04000100, length=2, flags=R | W),
    IOReg("TM0CNT_H", start=0x04000102, length=2, flags=R | W),
    IOReg("TM1CNT_L", start=0x04000104, length=2, flags=R | W),
    IOReg("TM1CNT_H", start=0x04000106, length=2, flags=R | W),
    IOReg("TM2CNT_L", start=0x04000108, length=2, flags=R | W),
    IOReg("TM2CNT_H", start=0x0400010A, length=2, flags=R | W),
    IOReg("TM3CNT_L", start=0x0400010C, length=2, flags=R | W),
    IOReg("TM3CNT_H", start=0x0400010E, length=2, flags=R | W),
    IOReg("SIODATA32", start=0x04000120, length=4, flags=R | W),
    IOReg("SIOMULTI0", start=0x04000120, length=2, flags=R | W),
    IOReg("SIOMULTI1", start=0x04000122, length=2, flags=R | W),
    IOReg("SIOMULTI2", start=0x04000124, length=2, flags=R | W),
    IOReg("SIOMULTI3", start=0x04000126, length=2, flags=R | W),
    IOReg("SIOCNT", start=0x04000128, length=2, flags=R | W),
    IOReg("SIOMLT_SEND", start=0x0400012A, length=2, flags=R | W),
    IOReg("SIODATA8", start=0x0400012A, length=2, flags=R | W),
    IOReg("KEYINPUT", start=0x04000130, length=2, flags=R),
    IOReg("KEYCNT", start=0x04000132, length=2, flags=R | W),
    IOReg("RCNT", start=0x04000134, length=2, flags=R | W),
    IOReg("JOYCNT", start=0x04000140, length=2, flags=R | W),
    IOReg("JOY_RECV", start=0x04000150, length=4, flags=R | W),
    IOReg("JOY_TRANS", start=0x04000154, length=4, flags=R | W),
    IOReg("JOYSTAT", start=0x04000158, length=2, flags=R),
    IOReg("IE", start=0x04000200, length=2, flags=R | W),
    IOReg("IF", start=0x04000202, length=2, flags=R | W),
    IOReg("WAITCNT", start=0x04000204, length=2, flags=R | W),
    IOReg("IME", start=0x04000208, length=2, flags=R | W),
    IOReg("POSTFLG", start=0x04000300, length=1, flags=R | W),
    IOReg("HALTCNT", start=0x04000301, length=1, flags=W),
]


class GBAView(BinaryView):
    name = "GBA"
    long_name = "GBA ROM View"
    entry_point = 0x08000000

    def __init__(self, data: BinaryView):
        BinaryView.__init__(self, parent_view=data, file_metadata=data.file)
        self.arch = Architecture["thumb2"]
        self.platform = Platform["gba-thumb2"]
        self.size = os.path.getsize(data.file.filename)

    def init(self):
        # Add ROM segment.
        self.add_auto_segment(
            0x08000000,
            0x01000000,
            0,
            self.size,
            SegmentFlag.SegmentReadable | SegmentFlag.SegmentExecutable,
        )
        self.add_auto_section(
            "ROM", 0x08000000, 0x01000000, SectionSemantics.ReadOnlyCodeSectionSemantics
        )

        for segment in _SEGMENTS:
            self.add_auto_segment(segment.start, segment.length, 0, 0, segment.flags)
            self.add_auto_section(segment.name, segment.start, segment.length)

        for ioreg in _IOREGS:
            self.define_auto_symbol(
                Symbol(SymbolType.DataSymbol, ioreg.start, ioreg.name)
            )

        self.add_entry_point(self.entry_point)
        return True

    @classmethod
    def is_valid_for_data(self, data):
        return data.file.filename.endswith(".gba")

    def perform_is_executable(self):
        return True

    def perform_get_entry_point(self):
        return self.entry_point


GBAView.register()
