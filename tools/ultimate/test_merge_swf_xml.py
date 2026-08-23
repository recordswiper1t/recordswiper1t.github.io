#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import merge_swf_xml as merge


class MergeSwfXmlTests(unittest.TestCase):
    def test_insertion_is_before_first_top_level_frame(self) -> None:
        xml = b'''<swf>
  <tags>
    <item type="DefineSpriteTag">
      <subTags>
        <item type="ShowFrameTag"/>
      </subTags>
    </item>
    <item type="ShowFrameTag"/>
    <item type="EndTag"/>
  </tags>
</swf>
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "base.xml"
            path.write_bytes(xml)
            pos = merge.find_insertion_point(path)
        self.assertEqual(xml[pos:].splitlines()[0], b'    <item type="ShowFrameTag"/>')

    def test_symbol_ids_and_names_remap_without_corrupting_flags(self) -> None:
        elem = ET.fromstring('''<item type="SymbolClassTag" forceWriteAsLong="false">
  <tags><item>2</item></tags>
  <names><item>Level</item></names>
</item>''')
        stats = Counter()
        merge.transform_tree(
            elem,
            {2: 22228},
            merge.ClassRenamer({"Level": "KR1__Level", "false": "KR1__false"}),
            stats,
        )

        self.assertEqual(elem.attrib["forceWriteAsLong"], "false")
        self.assertEqual([x.text for x in elem.find("tags").findall("item")], ["22228"])
        self.assertEqual([x.text for x in elem.find("names").findall("item")], ["KR1__Level"])
        self.assertEqual(stats["linkage_text_ids_remapped"], 1)

    def test_document_symbol_block_drops_its_preloader_bindings(self) -> None:
        elem = ET.fromstring('''<item type="SymbolClassTag">
  <tags><item>26</item><item>0</item></tags>
  <names><item>Preloader</item><item>Defense</item></names>
</item>''')
        stats = Counter()
        merge.drop_source_document_class(elem, stats)
        self.assertEqual(list(elem.find("tags")), [])
        self.assertEqual(list(elem.find("names")), [])
        self.assertEqual(stats["document_class_entries_removed"], 1)
        self.assertEqual(stats["document_preloader_linkage_entries_removed"], 2)


if __name__ == "__main__":
    unittest.main()
