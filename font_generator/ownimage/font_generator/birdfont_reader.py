import xml.etree.ElementTree as ET

class BirdfontReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = None
        self.root = None

    def load(self):
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    # ---------------- Unicode lookup ----------------

    def get_collection_by_unicode(self, char: str):
        codepoint = f"U+{ord(char):0X}"
        for coll in self.root.findall(".//collection"):
            if coll.get("unicode", "").upper() == codepoint:
                return coll
        return None

    def get_glyph_by_unicode(self, char: str):
        coll = self.get_collection_by_unicode(char)
        if coll is None:
            return None
        return coll.find("glyph")

    def get_layers_by_unicode(self, char: str):
        glyph = self.get_glyph_by_unicode(char)
        if glyph is None:
            return []
        return glyph.findall("layer")

    def get_paths_by_unicode(self, char: str):
        glyph = self.get_glyph_by_unicode(char)
        if glyph is None:
            return []
        paths = []
        for layer in glyph.findall("layer"):
            for p in layer.findall("path"):
                data = p.get("data")
                if data is not None:
                    paths.append(data)
        return paths

    # ---------------- Path modification ----------------

    def replace_paths_by_unicode(self, char: str, new_paths: list[str]):
        glyph = self.get_glyph_by_unicode(char)
        if glyph is None:
            raise ValueError(f"No glyph found for Unicode {char!r}")

        layers = glyph.findall("layer")
        if not layers:
            # If no layer exists, create one
            layer = ET.SubElement(glyph, "layer")
        else:
            # For simplicity, operate on the first layer
            layer = layers[0]

        # Remove existing paths from this layer
        for p in list(layer.findall("path")):
            layer.remove(p)

        # Add new paths
        for data in new_paths:
            ET.SubElement(layer, "path", {"data": data})

    def add_path_by_unicode(self, char: str, path_data: str):
        glyph = self.get_glyph_by_unicode(char)
        if glyph is None:
            raise ValueError(f"No glyph found for Unicode {char!r}")

        layers = glyph.findall("layer")
        if not layers:
            layer = ET.SubElement(glyph, "layer")
        else:
            layer = layers[0]

        ET.SubElement(layer, "path", {"data": path_data})

    def clear_paths_by_unicode(self, char: str):
        glyph = self.get_glyph_by_unicode(char)
        if glyph is None:
            raise ValueError(f"No glyph found for Unicode {char!r}")

        for layer in glyph.findall("layer"):
            for p in list(layer.findall("path")):
                layer.remove(p)

    # ---------------- Saving ----------------

    def save(self, out_filename: str | None = None):
        if out_filename is None:
            out_filename = self.filename
        self.tree.write(out_filename, encoding="utf-8", xml_declaration=True)


