# 本文件PWG格式生成部分代码引用自 open-print-stack (https://github.com/cskau/open-print-stack)
# 原始作者：cskau
# 对引用的部分代码进行了修改。


import io
from PIL import Image, ImageDraw
import struct


COLOR_SPACE_ENUM = {
    1: "Rgb",  # Device RGB (red green blue)
    3: "Black",  # Device black
    6: "Cmyk",  # Device CMYK (cyan magenta yellow black)
    18: "Sgray",  # sRGB grayscale
    19: "RGB",  # sRGB color
    20: "AdobeRgb",  # Adobe RGB color
    48: "Device1",  # Device color, 1 colorant
    49: "Device2",
    50: "Device3",
    51: "Device4",
    52: "Device5",
    53: "Device6",
    54: "Device7",
    55: "Device8",
    56: "Device9",
    57: "Device10",
    58: "Device11",
    59: "Device12",
    60: "Device13",
    61: "Device14",
    62: "Device15",
}

PRINT_QUALITY_ENUM = {
    0: "Default",
    3: "Draft",
    4: "Normal",
    5: "High",
}


def to_b(byte_val):
    """Convert byte to signed char (int)."""
    if isinstance(byte_val, int):
        return byte_val if byte_val <= 127 else byte_val - 256
    return struct.unpack("b", bytes([byte_val]))[0]


def to_B(byte_val):
    """Convert byte to unsigned char (int)."""
    if isinstance(byte_val, int):
        return byte_val
    return struct.unpack("B", bytes([byte_val]))[0]


class Raster:
    @staticmethod
    def create_best_raster():
        return PWG()

    def encode_packbits_like_(
        self,
        output_file,
        img,
        colorspace_str,
    ):
        img_out = img.convert(colorspace_str)
        x = 0
        y = 0
        to_x = 0
        while y < img_out.height:
            output_file.write(bytes([0x00]))
            while x < img_out.width:
                pixel = img_out.getpixel((x, y))
                to_x = x
                while (
                    (to_x + 1) < img_out.width
                    and pixel == img_out.getpixel((to_x + 1, y))
                    and (to_x - x) < 127
                ):
                    to_x += 1
                count = to_x - x
                output_file.write(bytes([count]))
                for channel in pixel:
                    output_file.write(bytes([channel]))
                x = to_x + 1
            x = 0
            y += 1

    def save(self, output_file):
        raise NotImplementedError()

    def load_img(self, input_img):
        raise NotImplementedError()


class PWG(Raster):
    """PWG Raster format, defined by [PWG5102.4]."""

    img = None
    media_color = ""
    media_type = ""
    print_content_optimize = ""
    cut_media = 0
    duplex = 1
    hw_resolution = (0, 0)
    insert_sheet = 0
    jog = 0
    leading_edge = 0
    media_position = 0
    media_weight_metric = 0
    num_copies = 1
    orientation = 0
    page_size = (0, 0)
    tumble = 0
    width = 0
    height = 0
    bits_per_color = 0
    bits_per_pixel = 0
    bytes_per_line = 0
    color_order = 0
    color_space = 0
    colorspace_str = "RGB"
    num_colors = 0
    total_page_count = 0
    cross_feed_transform = 0
    feed_transform = 0
    image_box_left = 0
    image_box_top = 0
    image_box_right = 0
    image_box_bottom = 0
    alternate_primary = (0, 255, 255, 255)
    print_quality = 0
    vendor_identifier = 0
    vendor_length = 0
    vendor_data = b""
    rendering_intent = ""
    page_size_name = ""

    def save(self):
        output_file = io.BytesIO()
        self.encode_header_(output_file)
        self.encode_packbits_like_(
            output_file,
            self.img,
            self.colorspace_str,
        )
        return output_file.getvalue()

    def load_img(self, input_img):
        self.img = input_img
        self.colorspace_str = "RGB"
        self.img = self.img.convert(self.colorspace_str)

        source_size = (self.img.width, self.img.height)
        self.hw_resolution = (600, 600)
        self.num_copies = 1
        self.page_size = (595, 842)  # A4 in points

        n_channels = 3
        self.width = 4961
        self.height = 7016

        if self.width != self.img.width or self.height != self.img.height:
            print("Size mismatch!")

        img2 = Image.new(
            mode=self.colorspace_str,
            size=(self.width, self.height),
            color=(255, 255, 255),
        )
        offset = (0, 0)
        img2.paste(
            self.img,
            box=(
                offset[0],
                offset[1],
                self.img.width + offset[0],
                self.img.height + offset[1],
            ),
        )
        self.img = img2

        self.bits_per_color = 8
        self.bits_per_pixel = self.bits_per_color * n_channels
        self.bytes_per_line = (self.bits_per_pixel // 8) * self.width

        self.color_space = 1
        self.num_colors = 3
        self.total_page_count = 1
        self.tumble = 0
        self.rendering_intent = "saturation"

        self.image_box_left = 0
        self.image_box_top = 0
        self.image_box_right = 0
        self.image_box_bottom = 0

        self.page_size_name = ""

    def encode_header_(self, output_file):
        output_file.write(b"RaS2")
        output_file.write(b"PwgRaster" + b"\0" * 55)

        encode_str = lambda s: s.encode("utf-8") + b"\0" * (64 - len(s.encode("utf-8")))
        output_file.write(encode_str(self.media_color))
        output_file.write(encode_str(self.media_type))
        output_file.write(encode_str(self.print_content_optimize))

        output_file.write(b"\0" * 12)
        output_file.write(struct.pack(">I", self.cut_media))
        output_file.write(struct.pack(">I", self.duplex))

        output_file.write(struct.pack(">I", self.hw_resolution[0]))
        output_file.write(struct.pack(">I", self.hw_resolution[1]))

        output_file.write(b"\0" * 16)
        output_file.write(struct.pack(">I", self.insert_sheet))
        output_file.write(struct.pack(">I", self.jog))
        output_file.write(struct.pack(">I", self.leading_edge))

        output_file.write(b"\0" * 12)
        output_file.write(struct.pack(">I", self.media_position))
        output_file.write(struct.pack(">I", self.media_weight_metric))

        output_file.write(b"\0" * 8)
        output_file.write(struct.pack(">I", self.num_copies))
        output_file.write(struct.pack(">I", self.orientation))

        output_file.write(b"\0" * 4)
        output_file.write(struct.pack(">I", self.page_size[0]))
        output_file.write(struct.pack(">I", self.page_size[1]))

        output_file.write(b"\0" * 8)
        output_file.write(struct.pack(">I", self.tumble))
        output_file.write(struct.pack(">I", self.width))
        output_file.write(struct.pack(">I", self.height))

        output_file.write(b"\0" * 4)
        output_file.write(struct.pack(">I", self.bits_per_color))
        output_file.write(struct.pack(">I", self.bits_per_pixel))
        output_file.write(struct.pack(">I", self.bytes_per_line))
        output_file.write(struct.pack(">I", self.color_order))
        output_file.write(struct.pack(">I", self.color_space))

        output_file.write(b"\0" * 16)
        output_file.write(struct.pack(">I", self.num_colors))

        output_file.write(b"\0" * 28)
        output_file.write(struct.pack(">I", self.total_page_count))
        output_file.write(struct.pack(">I", self.cross_feed_transform))
        output_file.write(struct.pack(">I", self.feed_transform))
        output_file.write(struct.pack(">I", self.image_box_left))
        output_file.write(struct.pack(">I", self.image_box_top))
        output_file.write(struct.pack(">I", self.image_box_right))
        output_file.write(struct.pack(">I", self.image_box_bottom))

        output_file.write(struct.pack("BBBB", *self.alternate_primary))
        output_file.write(struct.pack(">I", self.print_quality))

        output_file.write(b"\0" * 20)
        output_file.write(struct.pack(">I", self.vendor_identifier))
        output_file.write(struct.pack(">I", self.vendor_length))
        output_file.write(struct.pack("1088s", self.vendor_data))

        output_file.write(b"\0" * 64)

        intent_bytes = self.rendering_intent.encode("utf-8")[:64]
        output_file.write(intent_bytes + b"\0" * (64 - len(intent_bytes)))

        name_bytes = self.page_size_name.encode("utf-8")[:64]
        output_file.write(name_bytes + b"\0" * (64 - len(name_bytes)))


def create_cmyk_img(
    width=4961,
    height=7016,
    square_size=800,  # 每个色块边长
    row_index=0,  # 色块所在第几排（从 0 开始）
    row_gap=200,  # 行间距（每一排之间的垂直间隔）
    top_margin=200,  # 图像顶部到第0排的距离
    background=(255, 255, 255),
):
    """
    创建 CMYK 四色方块排成一行的 PNG。
    每个方块为 square_size x square_size。
    row_index 指色块所在的排号，0 为最上方第一排。
    """

    # CMYK -> RGB
    colors = [
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
        (255, 255, 0),  # Yellow
        (0, 0, 0),  # Black
    ]

    # 计算本排的 y 坐标（顶部偏移 + 行高 * row_index）
    y = top_margin + row_index * (square_size + row_gap)

    # 安全检查：方块是否超出画布
    if y + square_size > height:
        raise ValueError(
            f"第 {row_index} 排（y={y}）放不下方块，"
            f"画布高度={height}，方块高度={square_size}。"
        )

    # 计算四个方块的水平位置 — 自动均匀分布
    block_count = 4
    total_blocks_width = block_count * square_size
    available_space = width - total_blocks_width

    if available_space < 0:
        raise ValueError("画布宽度不足以容纳四个色块")

    # 均匀分布间隙：有5个间隔（左右两侧 + 三个内部间隔）
    gap = available_space / (block_count + 1)

    # 创建画布
    img = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(img)

    # 绘制 4 个色块
    for i, color in enumerate(colors):
        x = gap * (i + 1) + square_size * i
        x1 = int(x)
        y1 = int(y)
        draw.rectangle([x1, y1, x1 + square_size, y1 + square_size], fill=color)
    return img


def create_cmyk_pwg():
    """创建 CMYK 四色方块排成一行的 PWG 文件。"""
    img = create_cmyk_img(row_index=0)
    raster_obj = PWG()
    raster_obj.load_img(img)
    pwg_data = raster_obj.save()
    return pwg_data
